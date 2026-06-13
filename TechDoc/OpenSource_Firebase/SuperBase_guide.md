# Supabase 완전 가이드 (Full Version)

**버전:** 2026년 6월 기준  
**대상:** Vercel + Next.js 기반 풀스택 개발자

---

## 1. Supabase란?

Supabase는 **오픈소스 Firebase 대안**입니다. PostgreSQL 데이터베이스를 핵심으로 하여, 인증(Auth), 실시간(Realtime), 스토리지(Storage), 엣지 함수(Edge Functions) 등을 통합 제공하는 백엔드 플랫폼(BaaS)입니다.

- **오픈소스**: 모든 코드는 GitHub에 공개되어 있으며, 직접 호스팅할 수도 있습니다.
- **PostgreSQL 기반**: 관계형 데이터베이스의 강력함(JOIN, 트랜잭션, RLS 등)을 그대로 사용.
- **개발자 경험**: SDK(JavaScript, Flutter, Swift, Python 등) 및 CLI 제공, 빠른 프로토타이핑 가능.

---

## 2. 핵심 기능 (Core Features)

### 2.1 Database (PostgreSQL)

- **완전 관리형 PostgreSQL**: 버전 15.x, 설정 및 패치 자동화.
- **테이블 편집기**: 웹 UI에서 테이블 생성, SQL 편집, 관계 설정 가능.
- **SQL 에디터**: 온라인 SQL 쿼리 실행 및 히스토리 저장.
- **백업 & PITR**: 매일 자동 백업, 특정 시점 복구(Point-in-Time Recovery)는 Pro 이상.
- **스키마 마이그레이션**: `supabase migration` CLI로 버전 관리.

### 2.2 Authentication (Auth)

- **지원 로그인 방법**:
  - 이메일/비밀번호 (Magic Link 포함)
  - 소셜 OAuth: Google, Apple, GitHub, GitLab, Facebook, Discord, Slack, Kakao (일부 제공자)
  - 전화번호 SMS 인증 (Twilio 연동 필요)
  - 기업 SSO (SAML, Azure AD) – Enterprise 플랜
- **JWT 기반 세션**: 자동 갱신되는 액세스/리프레시 토큰.
- **Row Level Security (RLS) 통합**: 데이터베이스 정책에서 `auth.uid()` 직접 사용 가능.
- **사용자 관리 API**: 사용자 생성/삭제, 비밀번호 재설정, 이메일 변경 등.
- **이메일 템플릿 사용자 정의**: 가입 확인, 비밀번호 재설정 등의 이메일 내용 및 SMTP 설정 가능.

### 2.3 Storage

- **S3 호환 오브젝트 스토리지**: 이미지, 동영상, 파일 업로드.
- **버킷 정책 및 RLS**: 파일별 접근 권한을 RLS로 제어 가능.
- **이미지 변환**: `?width=200&height=200` 파라미터로 동적 리사이징 지원.
- **공개/비공개 버킷**: 서명된 URL을 통해 임시 접근 가능.

### 2.4 Realtime

- **웹소켓 기반 실시간 구독**: 테이블 변경 사항(INSERT, UPDATE, DELETE)을 클라이언트에 실시간 전송.
- **Broadcast**: 클라이언트 간 메시지 브로드캐스팅 (채팅, 공동 작업).
- **Presence**: 접속 중인 사용자 목록 관리 (실시간 사용자 상태).
- **PostgreSQL Change Data Capture (CDC)**: `REPLICA IDENTITY FULL` 설정 필요.

### 2.5 Edge Functions

- **Deno 기반 서버리스 함수**: 전 세계 엣지 노드에서 실행 (Vercel Edge Functions와 유사).
- **낮은 지연 시간**: JWT 인증, 결제 웹훅, AI API 프록시 등에 적합.
- **지원 언어**: TypeScript, JavaScript (Deno 런타임).
- **제한**: 실행 시간 10초 (무료), 메모리 150MB.

### 2.6 Vector (pgvector)

- **PostgreSQL 확장 pgvector 내장**: 임베딩 벡터 저장 및 유사도 검색 (코사인, 유클리드 등).
- **AI 애플리케이션**: RAG (Retrieval-Augmented Generation), 추천 시스템에 활용.

### 2.7 GraphQL (via pg_graphql)

- **자동 생성된 GraphQL API**: PostgreSQL 스키마를 기반으로 GraphQL 엔드포인트 제공.
- **필터, 정렬, 페이징** 지원.

---

## 3. 아키텍처 이해

Supabase는 여러 오픈소스 컴포넌트를 조합하여 만들어집니다.

| 컴포넌트 | 기술 | 역할 |
|----------|------|------|
| **Database** | PostgreSQL | 데이터 저장 및 쿼리 |
| **API** | PostgREST | RESTful API 자동 생성 |
| **Auth** | GoTrue | JWT 기반 인증 |
| **Storage** | Supabase Storage (S3 기반) | 파일 업로드/다운로드 |
| **Realtime** | Realtime server (Elixir) | 웹소켓 브로드캐스트 |
| **Edge Functions** | Supabase Edge Runtime (Deno) | 엣지 함수 실행 |
| **Dashboard** | Next.js 기반 웹 UI | 관리자 콘솔 |

- 모든 서비스는 **오픈소스**이며, 각각 분리되어 확장 가능.
- 클라이언트는 **하나의 API URL**로 모든 서비스에 접근 가능 (예: `https://<ref>.supabase.co`).

---

## 4. 장점 (Pros)

### Firebase 대비 우위

- **관계형 데이터베이스**: 복잡한 쿼리, JOIN, 트랜잭션 지원 (Firebase Firestore는 문서 기반).
- **가격 예측 가능성**: 사용자 수 기반 과금이 아니라 컴퓨팅 + 스토리지 + 대역폭 기반.
- **오픈소스**: 벤더 락인에서 자유로움, 자체 호스팅 가능.

### 개발자 생산성

- **15분 만에 인증 + DB 구축**: UI로 테이블 생성, RLS 정책 설정, 소셜 로그인 활성화.
- **자동 API 생성**: 테이블만 만들면 REST/GraphQL 엔드포인트 즉시 사용 가능.
- **TypeScript 지원**: `supabase gen types` 명령어로 DB 스키마 → TypeScript 타입 자동 생성.

### 보안 (RLS)

- **데이터베이스 레벨 권한**: RLS 정책으로 "사용자는 자신의 행만 볼 수 있음"과 같은 규칙을 SQL로 선언.
- **기본적으로 모든 API는 인증 필요**: `anon` 키는 제한적 접근, `service_role` 키만 전체 권한.

### 확장성

- **PostgreSQL 생태계 활용**: 인덱스, 뷰, 함수, 트리거, pg_cron, pgvector 등 확장.
- **스케일 업/아웃**: Pro 플랜 이상에서 전용 컴퓨트, 읽기 복제본, 분할 샤딩 준비 중.

### Vercel과의 완벽한 궁합

- **Vercel Marketplace 통합**: 1클릭으로 Supabase 프로젝트 생성 및 환경 변수 주입.
- **공식 `@supabase/ssr` 패키지**: Next.js App Router에서 쿠키 기반 세션 관리.
- **엣지 함수 간 유사성**: Vercel Edge Runtime과 Supabase Edge Functions 모두 Deno 기반 → 로직 재사용 용이.

### 무료 티어의 매력

- **50,000명 MAU** (월간 활성 사용자) – Firebase Auth 무료 티어보다 훨씬 넉넉함.
- **시간 제한 없음** – 12개월 후 요금이 갑자기 부과되지 않음.
- **500MB DB, 1GB 스토리지, 2GB 대역폭** – MVP, 사이드 프로젝트에 충분.

---

## 5. 단점 (Cons)

### 대역폭 병목 (무료 티어)

- **실질적 대역폭 한도 2GB**: 공식 문서에는 5GB로 표기되었으나, 커뮤니티 측정 결과 2GB 정도에서 제한 걸림.
- **영향**: 이미지, 비디오 위주 앱은 하루 만에 한도 초과 가능. API 응답 최적화 및 CDN 필수.

### Database Compute 성능 (무료 티어)

- **공유 CPU**: 피크 시간대 쿼리 지연 200~500ms 발생 가능.
- **연결 풀 제한**: 무료는 최대 50개 동시 연결, Pro는 200개.

### 소셜 로그인 제공자 제한

- **네이버(Naver), 카카오(Kakao), 라인(Line) 등 한국 서비스**: 기본 지원하지 않음 (OIDC Compliant 제공자로 연동 가능하나 설정 복잡).
- **중국 제공자 (WeChat, QQ)**: 없음.

### 커스터마이징 어려움 (관리형의 한계)

- **커스텀 도메인**: Pro 플랜 이상($25/월)에서만 가능.
- **JWT 만료 시간 변경 불가능**: 기본 1시간 (Google/Auth0 등은 15분 등 설정 가능).
- **SMTP 직접 설정 가능하나, 전문 이메일 발송 서비스 대비 부족** (마케팅 이메일, 대량 발송 기능 없음).

### 감사 로그 부재 (무료/Pro)

- **Enterprise에서만 감사 로그 제공**: 누가, 언제, 어떤 데이터에 접근했는지 로그를 확인하려면 $2,500/월.

### 벤더 락인 (약간)

- **RLS 정책**: Supabase의 `auth.uid()` 함수에 강하게 의존하면 다른 IdP로 이전 시 모든 정책 재작성 필요.
- **스토리지 URL 형식**: `https://<ref>.supabase.co/storage/v1/...` – 자체 도메인으로 전환 시 작업 필요.

### Realtime 성능 이슈 (대규모)

- **한 채널당 연결 수 제한**: 무료는 200개, Pro는 5,000개, 그 이상은 Redis 기반 확장 필요.
- **CDC 부하**: 변경 데이터 캡처가 많은 테이블에 사용 시 PostgreSQL WAL에 부하.

### Edge Functions 제약

- **실행 시간 10초**: 무거운 작업 (영상 인코딩, 대규모 데이터 처리) 불가.
- **외부 네트워크 접근 제한**: 무료에서는 일부 IP 대역만 허용 (Pro에서 해제).
- **로컬 디버깅 어려움**: `supabase functions serve`는 느리고, VSCode 디버거 연동 불안정.

---

## 6. Vercel + Supabase 통합 가이드

### 6.1 기본 설정 (5분)

1. **Vercel 대시보드** → Integrations → Supabase → "Connect" 클릭.
2. 새 Supabase 프로젝트 생성 또는 기존 프로젝트 선택.
3. 환경 변수 (`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`) 자동 주입.
4. `@supabase/ssr` 패키지 설치:

```bash
npm install @supabase/supabase-js @supabase/ssr
```

### 6.2 미들웨어 설정 (`middleware.ts`)

```typescript
import { createMiddlewareClient } from '@supabase/ssr'
import { NextResponse } from 'next/server'

export async function middleware(req) {
  const res = NextResponse.next()
  const supabase = createMiddlewareClient({ req, res })
  await supabase.auth.getSession()
  return res
}
```

> **참고**: `createMiddlewareClient`는 `@supabase/ssr` v0.1.0 이상에서 사용합니다. 구버전 `@supabase/auth-helpers-nextjs`와 혼용하지 마세요.

### 6.3 Supabase 클라이언트 초기화

서버 컴포넌트와 클라이언트 컴포넌트에서 각각 다른 방식으로 초기화합니다.

**서버 컴포넌트 (Server Component)**

```typescript
import { createServerComponentClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export default async function Page() {
  const supabase = createServerComponentClient({ cookies })
  const { data: { session } } = await supabase.auth.getSession()
  // ...
}
```

**클라이언트 컴포넌트 (Client Component)**

```typescript
'use client'
import { createClientComponentClient } from '@supabase/ssr'

export default function Component() {
  const supabase = createClientComponentClient()
  // ...
}
```

### 6.4 Google OAuth 설정 (대시보드에서 3분)

1. Supabase 대시보드 → Authentication → Providers → Google 활성화.
2. Client ID / Secret 입력 → 리디렉션 URL 복사하여 Google Cloud Console에 등록.

### 6.5 RLS 예제 (게시판)

```sql
-- 테이블 생성
CREATE TABLE posts (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id uuid REFERENCES auth.users(id),
  content text,
  created_at timestamptz DEFAULT now()
);

-- RLS 활성화
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- 정책: 사용자는 자신의 글만 볼 수 있음
CREATE POLICY "Users can view own posts" ON posts
  FOR SELECT USING (auth.uid() = user_id);

-- 정책: 로그인한 사용자만 글 작성 가능
CREATE POLICY "Authenticated users can insert" ON posts
  FOR INSERT WITH CHECK (auth.role() = 'authenticated');
```

### 6.6 TypeScript 타입 생성

```bash
npx supabase gen types typescript --project-id <ref> > types/supabase.ts
```

생성된 타입을 쿼리에 활용하면 컴파일 타임에 스키마 오류를 잡을 수 있습니다.

```typescript
import { Database } from '@/types/supabase'

const supabase = createClientComponentClient<Database>()
const { data } = await supabase.from('posts').select('*')
// data는 Database['public']['Tables']['posts']['Row'][] 타입으로 추론됨
```

### 6.7 환경 변수 관리

로컬 개발 시 `.env.local`에 아래를 추가합니다. Vercel 통합을 사용하면 프리뷰/프로덕션 환경 변수는 자동 주입됩니다.

```bash
NEXT_PUBLIC_SUPABASE_URL=https://<ref>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon-key>
# 절대 클라이언트에 노출하지 말 것
SUPABASE_SERVICE_ROLE_KEY=<service-role-key>
```

---

## 7. 가격 정책 (2026년 6월 기준)

| 플랜 | 가격 | MAU | DB 용량 | 대역폭 | Edge Functions | 실시간 연결 |
|------|------|-----|---------|--------|----------------|------------|
| Free | $0 | 50,000 | 500MB | 2GB | 50만 호출/월 | 200 |
| Pro | $25 | 100,000 | 8GB | 100GB | 200만 호출/월 | 5,000 |
| Team | $599 | 500,000 | 40GB | 400GB | 500만 호출/월 | 20,000 |
| Enterprise | 커스텀 | 무제한 | 무제한 | 무제한 | 무제한 | 무제한 |

**추가 비용:**

- 초과 DB 스토리지: $0.125/GB (Pro 이상)
- 초과 대역폭: $0.09/GB (Pro 이상)
- 추가 에지 함수 호출: $2/백만 회

> **참고:** 무료 티어는 프로젝트당 2개로 제한, Pro는 조직당 프로젝트 수 무제한.

---

## 8. Supabase를 선택해야 하는 경우

### 적합한 프로젝트

- **MVP, 스타트업 초기 제품**: 빠른 개발 속도와 무료 티어의 넉넉한 MAU.
- **Vercel + Next.js 풀스택**: 공식 통합으로 개발자 경험 최적화.
- **관계형 데이터가 중심인 앱**: 주문, 예약, 재고 관리 등 복잡한 쿼리 필요.
- **RLS로 데이터 보안을 강화해야 하는 서비스**: 의료, 금융, 개인정보 처리.
- **실시간 기능이 필요한 앱**: 채팅, 협업 툴, 대시보드.
- **AI/벡터 검색 앱**: pgvector 내장으로 별도 벡터 DB 없이 RAG 구현 가능.

### 부적합한 프로젝트

- **미디어 대역폭이 큰 앱 (사진/동영상)**: 대역폭 과금이 부담스러움. 대신 Vercel Blob Storage 또는 Cloudflare R2 고려.
- **한국 소셜 로그인(네이버, 카카오) 필수**: Auth.js 또는 Passport.js 직접 구현이 더 간편.
- **엔터프라이즈 감사 로그 및 SSO 필요**: Auth0, WorkOS, Clerk이 더 적합.
- **서버리스 함수로 긴 작업(>10초)**: 백그라운드 Worker가 필요한 경우 별도 서버 필요.

---

## 9. Supabase vs 경쟁사 비교

| 특징 | Supabase | Firebase | Auth0 | Clerk |
|------|----------|----------|-------|-------|
| 데이터베이스 | PostgreSQL | Firestore (NoSQL) | 없음 | 없음 |
| 인증 무료 MAU | 50k | 50k (사용자 기준) | 7,500 | 10k |
| 실시간 | 지원 (WebSocket) | 지원 | 미지원 | 미지원 |
| 스토리지 | 지원 (S3 호환) | 지원 | 미지원 | 미지원 |
| 오픈소스 | 전체 공개 | 미공개 | 미공개 | 미공개 |
| 자체 호스팅 | 지원 (Docker) | 미지원 | 미지원 | 미지원 |
| 가격 예측성 | 보통 (사용량별) | 낮음 (요청당) | 높음 (MAU당) | 중간 (MAU+기능) |
| 커스텀 도메인 | Pro 이상 | Blaze 요금제 이상 | 표준 이상 | Pro 이상 |
| pgvector / 벡터 검색 | 내장 | 미지원 | 미지원 | 미지원 |

---

## 10. 자주 묻는 질문 (FAQ)

**Q: Supabase 무료 티어에서 네이버 로그인을 쓸 수 있나요?**  
A: 직접 구현은 가능하나 복잡합니다. Auth.js (NextAuth)를 함께 사용하는 것이 더 간단합니다.

**Q: Vercel에서 Supabase로 직접 연결해도 안전한가요?**  
A: 네. `NEXT_PUBLIC_SUPABASE_ANON_KEY`는 기본적으로 안전하지만, RLS로 데이터를 보호해야 합니다. `service_role` 키는 절대 클라이언트에 노출하지 마세요.

**Q: Supabase로 이메일 마케팅(뉴스레터)을 보낼 수 있나요?**  
A: SMTP를 연결할 수 있으나 대량 발송용이 아닙니다. Resend, SendGrid, Brevo 같은 전문 서비스를 사용하세요.

**Q: 프로덕션에서 무료 티어를 써도 될까요?**  
A: 사용자가 적고(MAU < 5,000), 대역폭이 작다면 가능합니다. 하지만 트래픽 급증 시 유료 전환을 고려하세요.

**Q: Supabase를 자체 호스팅하면 완전 무료인가요?**  
A: 서버 비용(클라우드 VM 또는 온프레미스)은 발생합니다. 관리 오버헤드도 크므로, 소규모에서는 관리형이 더 경제적입니다.

**Q: pgvector로 RAG를 구현하려면 어떤 플랜이 필요한가요?**  
A: 무료 플랜에서도 pgvector 확장을 활성화할 수 있습니다. 단, 임베딩 벡터 수가 많아지면 DB 용량 500MB 한도에 주의해야 합니다.

**Q: Connection Pooling은 어떻게 설정하나요?**  
A: Supabase는 PgBouncer를 내장하고 있습니다. 연결 문자열에서 포트를 `5432`(직접 연결) 대신 `6543`(Pooler 모드)으로 변경하면 됩니다. Serverless 환경(Next.js API Routes, Edge Functions)에서는 반드시 Pooler를 사용하세요.

---

## 11. 추가 학습 자료

- **공식 문서**: [supabase.com/docs](https://supabase.com/docs)
- **Vercel 통합**: [vercel.com/integrations/supabase](https://vercel.com/integrations/supabase)
- **GitHub 저장소**: [github.com/supabase/supabase](https://github.com/supabase/supabase)
- **Discord 커뮤니티**: [discord.supabase.com](https://discord.supabase.com)
- **Supabase YouTube 채널**: 공식 튜토리얼 및 릴리즈 노트 영상 제공

---

## 12. 결론

Supabase는 오픈소스의 자유로움과 관리형 서비스의 편의성을 절묘하게 결합한 플랫폼입니다. Vercel과의 시너지, PostgreSQL의 강력함, 넉넉한 무료 티어 덕분에 개인 개발자부터 스타트업까지 널리 사랑받고 있습니다.

다만, 대역폭 제한과 한국 소셜 로그인 지원의 미비함은 명확한 단점입니다. 프로젝트의 요구 사항을 저울질하여 Supabase를 도입할지, 대체제를 고민할지 결정하시기 바랍니다.

"Supabase는 단순한 Firebase 대체제를 넘어, 오픈소스 생태계의 새로운 표준이 되어가고 있습니다."
