# CASSANDRA AI — 기술 스택

> 실제 운영 인프라 기준. 모든 계층이 **무료 티어(Free Tier)** 정책 안에서 운영된다.

---

## 인프라 아키텍처

```
[사용자 브라우저]
       │
       ▼
┌──────────────────────────────────────────┐
│  Vercel Edge Network (Global CDN)         │
│  ┌────────────┐  ┌──────────────────────┐ │
│  │ Static     │  │ Vercel WAF           │ │
│  │ Assets     │  │ (DDoS·Bot·Rate Limit) │ │
│  └────────────┘  └──────────────────────┘ │
│       │                    │               │
│       ▼                    ▼               │
│  ┌────────────────────────────────────┐   │
│  │  Next.js 15 Server (App Router)     │   │
│  │  ┌──────────┐  ┌─────────────────┐ │   │
│  │  │ API Routes│  │ React Server    │ │   │
│  │  │ (Edge/λ)  │  │ Components (RSC)│ │   │
│  │  └──────────┘  └─────────────────┘ │   │
│  └────────┬───────────────┬───────────┘   │
└───────────┼───────────────┼───────────────┘
            │               │
     ┌──────▼──────┐  ┌─────▼──────────┐
     │ Neon.tech   │  │ Vercel KV      │
     │ PostgreSQL  │  │ (Redis)        │
     │ (Serverless)│  │ Cache·Rate Lim │
     └──────┬──────┘  └────────────────┘
            │
     ┌──────▼──────┐
     │ DART API    │
     │ (OpenDART)  │
     └─────────────┘
```

---

## 계층별 상세

### 1. 배포 & 호스팅 — Vercel

| 항목 | 내용 |
|---|---|
| **플랜** | Hobby (무료) |
| **프레임워크** | Next.js 15 App Router |
| **서버리스 함수** | Vercel Functions (Node.js 22.x, 10s 기본 타임아웃) |
| **Edge Functions** | 전 세계 100+ PoP에서 실행 (검색·경량 API) |
| **정적 자산** | Vercel Edge CDN (`.next/static`, 이미지, 폰트) |
| **도메인** | `*.vercel.app` (무료 도메인) 또는 커스텀 도메인 |
| **빌드** | Git push → Vercel 자동 빌드 (`next build`) |
| **환경변수** | Vercel Dashboard에서 주입 (`.env` 불필요) |

**Hobby 플랜 제한:**
- 월 대역폭 100GB
- 빌드 시간 100시간/월
- 서버리스 함수 실행 시간 10s (기본값, Pro에서 60s로 확장)
- 동시 함수 실행 12개

### 2. CDN & WAF — Vercel Edge Network

| 기능 | 설명 |
|---|---|
| **CDN** | 전 세계 100+ PoP, 자동 캐싱. `Cache-Control` 헤더로 TTL 제어. |
| **WAF** | Vercel WAF — IP 기반 Rate Limiting, Bot Detection, DDoS 완화. `vercel.json`에서 커스텀 룰 설정 가능. |
| **DDoS** | Layer 3/4/7 공격 자동 차단 (Hobby 플랜 기본 포함) |
| **SSL/TLS** | Let's Encrypt 자동 발급·갱신, HTTP/2 + HTTP/3 지원 |

```jsonc
// vercel.json 예시 (WAF 커스텀 룰)
{
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "Strict-Transport-Security", "value": "max-age=63072000" }
      ]
    }
  ],
  "functions": {
    "src/app/api/**/*.ts": {
      "maxDuration": 10
    }
  }
}
```

### 3. 데이터베이스 — Neon.tech

| 항목 | 내용 |
|---|---|
| **플랜** | Free Tier |
| **엔진** | Serverless PostgreSQL 16 |
| **스토리지** | 0.5GB (무료) |
| **커넥션** | 풀링 내장 (PgBouncer), 최대 100 동시접속 |
| **브랜치** | DB Branching (PR별 격리 환경 가능) |
| **백업** | Point-in-Time Recovery (PITR), 1일 보존 (무료) |
| **리전** | ap-northeast-2 (서울) 또는 ap-northeast-1 (도쿄) |
| **연결 방식** | `DATABASE_URL` 환경변수 → Prisma 연결 |

**Free Tier 제한:**
- 월 컴퓨트 190시간 (약 0.25 vCPU 상시)
- 스토리지 0.5GB → 프로젝트 성숙 시 Pro로 마이그레이션 계획
- 동시접속 100 → PgBouncer 풀링으로 커버

> **참고**: 로컬 개발 시 TimescaleDB(`timescale/timescaledb:latest-pg16`, Docker Compose)를 사용하지만, Neon.tech는 TimescaleDB 확장을 지원하지 않아 **프로덕션은 표준 PostgreSQL**로 운영한다. 시계열 쿼리(`MarketSnapshot` 등)는 표준 SQL로 대체.

### 4. 캐시 — Vercel KV (Redis)

| 항목 | 내용 |
|---|---|
| **플랜** | Hobby (무료) |
| **저장 용량** | 256MB |
| **월 요청** | 60,000회 (무료) |
| **API** | `@vercel/kv` — Redis 호환, REST API 기반 |
| **활용** | 검색 결과 캐시, 레이트 리미트, 실시간 검색어 순위 |

```typescript
// 예시: 검색 결과 캐싱
import { kv } from '@vercel/kv';

const cacheKey = `search:${query}`;
const cached = await kv.get(cacheKey);
if (cached) return cached;

const result = await db.query(query);
await kv.set(cacheKey, result, { ex: 300 }); // 5분 TTL
return result;
```

### 5. ORM — Prisma 6

| 항목 | 내용 |
|---|---|
| **스키마** | `prisma/schema.prisma` — 12개 모델 정의 |
| **클라이언트** | `@prisma/client` ^6.0.0 |
| **마이그레이션** | `npx prisma migrate dev` |
| **타입 안전성** | 자동 생성 타입으로 풀스택 TypeScript 연동 |
| **리레이션** | Corp ↔ Person ↔ Fund 3중 관계, Filing·Signal 연결 |

### 6. 애플리케이션 레이어

| 계층 | 기술 | 버전 | 용도 |
|---|---|---|---|
| **프레임워크** | Next.js | 15.x | App Router, RSC, API Routes |
| **언어** | TypeScript | 5.x | 정적 타입, 풀스택 일관성 |
| **UI 프레임워크** | React | 19.x | 클라이언트 컴포넌트 |
| **스타일링** | Tailwind CSS | 4.x | Utility-first, PostCSS 기반 |
| **시각화** | Cytoscape.js | 3.30.x | 인터랙티브 관계망 그래프 |
| **상태 관리** | Zustand | 5.x | 클라이언트 상태 (핀보드 등) |
| **서버 상태** | TanStack React Query | 5.x | API 호출 캐싱·동기화 |
| **밸리데이션** | Zod | 3.x | API 입출력 검증 |
| **UI 컴포넌트** | Radix UI | — | Headless 접근성 컴포넌트 |
| **아이콘** | Lucide React | 0.4xx | SVG 아이콘 |
| **날짜** | date-fns | 4.x | 날짜 변환·포맷 |
| **웹 스크래핑** | Puppeteer | 25.x | Naver Finance 크롤링 |
| **HTML 파싱** | Cheerio | 1.x | 경량 HTML 파서 |

### 7. LLM — 다중 모델 앙상블

| 모델 | 제공사 | 역할 |
|---|---|---|
| **DeepSeek V3** | DeepSeek | 1차 분석 (비용 효율적, 한국어 특화) |
| **Claude Sonnet 4** | Anthropic | 2차 교차검증 (문맥 추론·판단 보강) |

- **호출 방식**: API Route → LLM API (Server-side only, 토큰 미노출)
- **앙상블 모드**: 순차 fallback 또는 다수결 교차검증
- **비용 통제**: 분석 건당 토큰 제한 + 결과 캐싱 (Vercel KV)

### 8. 외부 데이터 소스

| 소스 | 용도 | 한도 |
|---|---|---|
| **OpenDART API** | 금융감독원 전자공시 수집 | 일 10,000건 (실제 사용량 ~300건/일) |
| **Naver Finance** | 시장 스냅샷 크롤링 (거래량·검색어) | Puppeteer 기반, 30분 간격 |
| **KIND (한국거래소)** | 상장폐지·관리종목 이력 (계획) | — |

### 9. 개발 도구

| 도구 | 용도 |
|---|---|
| **tsx** | TypeScript 직접 실행 (시드, 스크립트) |
| **PostCSS + Autoprefixer** | CSS 후처리 |
| **Prisma Studio** | GUI 기반 DB 브라우징 (`npx prisma studio`) |
| **Docker Compose** | 로컬 PostgreSQL + TimescaleDB |

---

## 무료 티어 비용 정리

| 서비스 | 플랜 | 월 비용 | 한계 |
|---|---|---|---|
| **Vercel** | Hobby | $0 | 대역폭 100GB, 빌드 100h, 함수 실행 10s |
| **Neon.tech** | Free | $0 | 0.5GB 스토리지, 190h 컴퓨트 |
| **Vercel KV** | Hobby | $0 | 256MB, 60K 요청 |
| **OpenDART** | 무료 API | $0 | 일 10,000건 |
| **DeepSeek API** | 종량제 | ~$5/월 | 분석 결과 캐싱으로 최적화 |
| **Claude API** | 종량제 | ~$10/월 | 교차검증에만 사용 |
| **합계** | | **~$15/월** | LLM 호출량에 따라 변동 |

> LLM 비용을 제외한 **인프라 비용은 $0**이다. LLM 호출량은 Vercel KV 캐싱 + 일일 분석 건수 제한으로 상한 통제.

---

## 환경 변수

```
# Database
DATABASE_URL="postgresql://..."             # Neon.tech 연결 문자열

# Cache
KV_URL="https://..."                        # Vercel KV REST API
KV_REST_API_URL="https://..."
KV_REST_API_TOKEN="..."

# DART
DART_API_KEY=...                            # OpenDART API 키

# LLM
DEEPSEEK_API_KEY=sk-...                     # DeepSeek API
ANTHROPIC_API_KEY=sk-ant-...                # Claude API

# App
NEXT_PUBLIC_APP_NAME="CASSANDRA AI"
```

모든 환경변수는 **Vercel Dashboard → Settings → Environment Variables**에서 주입하며, 로컬 개발 시에만 `.env.local`을 사용한다 (`.gitignore`).

---

## 배포 파이프라인

```
GitHub Push (main)
       │
       ▼
Vercel Git Integration (자동 감지)
       │
       ▼
npm install → prisma generate → next build
       │
       ├── Static Assets → Vercel Edge CDN
       ├── Serverless Functions → Vercel Functions
       └── Prisma Client → Neon.tech 연결
       │
       ▼
Preview Deployment (PR별) / Production Deployment (main)
```
