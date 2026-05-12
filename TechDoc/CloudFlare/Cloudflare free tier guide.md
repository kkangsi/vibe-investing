# Cloudflare 무료 티어 가입 가이드

> Azure -> CloudFlare 용도 관점에서 작성. Azure Functions + Blob Storage 의 기존 architecture 마이그레이션 검토용.

---

## 1. 가입 단계 — 3분 소요

### Step 1. 계정 생성

1. https://dash.cloudflare.com/sign-up 접속
2. 이메일 + 비밀번호 입력 (또는 GitHub 계정 SSO 가능)
3. 이메일 인증 (스팸함도 확인)

신용카드 입력 없음. Workers / Pages / R2 / KV 무료 티어 모두 신용카드 없이 즉시 사용 가능.

### Step 2. 도메인 추가 (선택)

기존 도메인이 있다면:

1. Dashboard → Add a Site
2. 도메인 입력 → Free plan 선택
3. Nameserver 변경 (도메인 등록업체에서 Cloudflare 의 ns1/ns2 로)

기존 도메인 없으면 건너뛰어도 됩니다. `*.workers.dev` 또는 `*.pages.dev` subdomain 사용 가능.

### Step 3. 2FA 활성화 (필수 권장)

1. My Profile → Authentication
2. Two-factor Authentication → Enable
3. Google Authenticator 또는 Authy 등록

Cloudflare 계정 hijack 시 모든 서비스 영향. 2FA 는 옵션 아닌 필수.

---

## 2. 무료 한도 — 증권당 용도 관점

### Workers (서버리스 함수)

| 항목 | 무료 한도 | 증권당 추정 사용량 |
| --- | --- | --- |
| Requests | 100,000/day | DAU 1,000 × 100 req = 100K (한계 근접) |
| CPU time per request | 10ms | LLM call 은 wait 시간 (CPU 시간 아님), 안전 |
| Subrequests | 50/invocation | 충분 |
| Script size | 1 MB | 충분 |

DAU 1,000 까지는 무료 가능. DAU 5,000+ 시 Workers Paid ($5/mo) 전환 필요.

### Workers KV (key-value cache)

| 항목 | 무료 한도 | 증권당 사용 |
| --- | --- | --- |
| Reads | 100,000/day | cache hit 80% × DAU 1,000 × 100 req = 80K (안전) |
| Writes | 1,000/day | LLM 응답 새로 caching 시 사용 |
| Deletes | 1,000/day | 충분 |
| List | 1,000/day | 거의 사용 안 함 |
| Storage | 1 GB | text-only cache 라면 충분 |
| Value size limit | 25 MB/key | LLM 응답 1개당 수 KB, 충분 |

80% cache hit rate 운영 시 완전히 무료 한도 안에 들어옴.

### R2 (object storage, Azure Blob 대체)

| 항목 | 무료 한도 | 증권당 사용 |
| --- | --- | --- |
| Storage | 10 GB | Azure Blob 현재 사용량 추정 1 GB 미만 |
| Class A operations (writes) | 1,000,000/month | 충분 |
| Class B operations (reads) | 10,000,000/month | 매우 충분 |
| Egress (bandwidth) | 무제한 무료 | 결정적 차별점 |

egress 무료가 R2 의 가장 큰 장점. Azure Blob 의 egress 요금 부담 사라짐.

### Pages (정적 사이트)

| 항목 | 무료 한도 |
| --- | --- |
| Bandwidth | 무제한 |
| Builds | 500/month |
| Concurrent builds | 1 |
| Custom domains | 100 |
| Sites | unlimited |

증권당 frontend 호스팅에 완전히 충분. Azure Static Web Apps 와 동등.

### Workers AI (선택 사용)

| 항목 | 무료 한도 |
| --- | --- |
| Neurons | 10,000/day (≈ 5,000-10,000 requests) |
| Models | Llama 3.x, DeepSeek 등 |

본인이 DeepSeek V3.1 직접 API 사용 중이면 Workers AI 불필요. 다만 대체 LLM 으로 백업 가능.

### Reset 시점

모든 무료 한도 reset: 매일 UTC 00:00 (한국시간 09:00)

---

## 3. 증권당 용도별 권장 setup

### 단계 1. 정적 자산만 마이그레이션 (low-risk, 2-3시간)

```
Azure Static Web Apps → Cloudflare Pages
- Frontend (HTML/CSS/JS) Pages 에 배포
- LLM 호출은 Azure Functions 그대로 유지
- 변경: API endpoint URL 만 frontend 에서 업데이트
```

- 위험: 매우 낮음 (frontend 만 이동)
- 효과: 한국 사용자 첫 페이지 load 50-100ms 단축

### 단계 2. R2 로 Blob 마이그레이션 (런칭 후 권장)

```
Azure Blob Storage → Cloudflare R2
- Super Slurper 또는 Sippy 로 자동 마이그레이션
- S3 호환 API 이므로 코드 변경 최소
- egress 비용 절감 효과 큼
```

- 위험: 중간 (URL 구조 변경)
- 효과: egress 무료화 + edge cache 강화

### 단계 3. Workers 로 함수 이동 (런칭 14일 후 검토)

```
Azure Functions (Python) → Cloudflare Workers (JS/TS or Python WASM)
- DeepSeek API call 을 fetch() 로 재작성
- 4-tier cache 를 Workers KV + Cache API 로 재설계
```

- 위험: 높음 (runtime 환경 다름)
- 효과: cold start 사라짐, edge latency 추가 단축
- 권장 시점: 5/28 이후 (런칭 + 14일 burn-in 데이터 기반)

---

## 4. 가입 후 첫 설정 — 5분

### Wrangler CLI 설치 (Workers/Pages 배포 도구)

```bash
# Node.js 18+ 필요
npm install -g wrangler

# 로그인 (브라우저 인증)
wrangler login

# 확인
wrangler whoami
```

### Pages 첫 배포 (정적 사이트 테스트)

```bash
# Git 연동
# Dashboard → Pages → Connect to Git
# GitHub 레포 연결 → main branch 자동 빌드

# 또는 직접 배포
wrangler pages deploy ./build --project-name=jeunggwon-test
```

배포 후 URL: `https://jeunggwon-test.pages.dev`

### R2 버킷 첫 생성

```bash
# 무료 한도 안에서 버킷 생성
wrangler r2 bucket create jeunggwon-blob

# 파일 업로드 테스트
wrangler r2 object put jeunggwon-blob/test.txt --file ./test.txt
```

---

## 5. 주의사항 4가지

### 주의 1. Workers 의 Python 지원 제한적

```
지원: Pyodide 기반 WASM (제한된 stdlib)
미지원: native C 의존 패키지 (numpy 일부, asyncio)
```

본인 증권당 코드가 어떤 Python 패키지 의존하는지 확인 필요. 순수 Python + fetch 라면 이식 가능, 복잡한 의존성 이면 JavaScript/TypeScript 재작성 필요.

### 주의 2. KV consistency 는 eventual

```
KV 쓰기 → 다른 edge location 에서 최대 60초 후 읽기 가능
즉시 일관성 필요한 데이터 (예: 사용자 세션) 에는 부적합
```

사용자 세션 같은 strong consistency 필요한 데이터는 Durable Objects 사용 (Workers Paid $5/mo 필요).

### 주의 3. Free 한도 daily reset 의 risk

```
Workers requests 100K/day = 시간당 평균 4,166 req
peak hour (예: 미장 마감 직후 22:30 KST) 에 시간당 10K req 발생 시
→ 100K 한도 오후에 소진
→ 다음 UTC 00:00 (한국시간 09:00) 까지 서비스 중단
```

peak hour 모니터링 필수. 증권당 미장 마감 직후 traffic spike 가 한도 초과 위험. 사용자 1,000 명 시점에 Workers Paid ($5/mo) 전환 권장.

### 주의 4. DeepSeek API call latency 가 bottleneck

```
Cloudflare edge: 10-50ms
DeepSeek API: 2,000-8,000ms (LLM inference)
사용자 체감 latency: 95% 이상이 LLM call
```

Cloudflare 마이그레이션의 체감 효과는 first-page-load 에 집중. LLM 응답 시간 자체는 변화 없음. 마이그레이션 ROI 계산 시 정직하게 반영 필요.

---

## 5. 참고 자료

- 가입: https://dash.cloudflare.com/sign-up
- Workers 무료 한도: https://developers.cloudflare.com/workers/platform/pricing/
- R2 무료 한도: https://developers.cloudflare.com/r2/pricing/
- KV 무료 한도: https://developers.cloudflare.com/kv/platform/pricing/
- Pages 무료 한도: https://www.cloudflare.com/plans/developer-platform/
- Wrangler CLI: https://developers.cloudflare.com/workers/wrangler/
- Super Slurper (S3 → R2 마이그레이션): https://developers.cloudflare.com/r2/data-migration/super-slurper/
