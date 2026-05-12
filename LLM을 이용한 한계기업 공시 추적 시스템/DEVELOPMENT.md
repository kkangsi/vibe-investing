# 개발 문서: 한계기업 공시 관계망 추적 서비스

> DART 공시 기반 인물·법인 관계망 추적, 결합 신호 탐지, 텔레그램 미니앱을 통한 언론사 대상 알림 서비스.

| 항목 | 값 |
|---|---|
| 문서 버전 | v0.1 |
| 작성일 | 2026-05-12 |
| 호스팅 | OCI Always Free (ARM Ampere A1) |
| 사용자 채널 | Telegram Mini App + Telegram Bot 푸시 |
| 가입 자격 | 등록 언론사 도메인 이메일 인증자 |
| 모니터링 풀 | 시총 500억 원 미만 코스닥 100종목 |
| 집중 모니터링 | 그 중 단기 거래량 spike 상위 10종목 |

관련 문서: `HYPOTHESIS.md`

---

## 0. 시스템 개요

### 0.1 목적

코스닥 시총 500억 원 미만 한계기업 100종목 풀에서 무자본 M&A·CB 발행·임원변경 등 공시 이벤트의 **결합 패턴**을 실시간 탐지하고, 등록 언론사에 텔레그램 미니앱과 봇 푸시로 전달.

### 0.2 비기능 요구사항

| 항목 | 목표 |
|---|---|
| 공시 발생 → 알림 지연 | ≤ 10분 (장 시간 기준) |
| 일일 비용 | $0 (OCI Always Free + Claude Haiku 저비용 호출) |
| 사용자 수 | v0.x 단계 ≤ 200명 (언론사) |
| 가용성 | 95% (단일 VM, best effort) |
| 백업 | nightly pg_dump → Object Storage, 14일 보존 |

---

## 1. 사용자 시나리오

### 1.1 가입

1. 기자가 텔레그램에서 `@your_bot_name` 검색 → `/start`
2. 봇이 "언론사 가입 안내" + Mini App 버튼 노출
3. 미니앱에서 언론사 이메일 입력
4. 인증 코드 발송 → 입력 → 도메인 화이트리스트 확인
5. 자동 승인 또는 admin review queue
6. 승인 완료 → 일일 리포트 자동 구독

### 1.2 일상 사용

- **매일 16:00 KST**: 당일 거래 종료 후 신호 발생 종목 1~3개를 텔레그램 푸시
- **18:00 KST**: 일일 리포트 (당일 100풀의 주요 이벤트 요약, top 10 거래량 spike, 신규 공시)
- **수시**: High signal 룰 발화 시 즉시 푸시
- 푸시 메시지 클릭 → 미니앱 deep link → 종목 상세 그래프 뷰

### 1.3 미니앱 뷰

- 홈: 오늘의 watchlist (top 10), 누적 신호 점수 상위
- 종목 상세: 공시 타임라인, 인물·법인 그래프, 신호 발화 이력
- 인물 상세: 자연인의 등기 이력 회사 리스트 (사실 적시만, 평가 없음)
- 검색: corp_code, 회사명, 자연인 이름

---

## 2. 모니터링 유니버스 정의

### 2.1 100종목 풀 (일 1회 갱신)

매일 08:30 KST 갱신. 다음 우선순위 룰로 100개 선정.

```sql
WITH candidates AS (
  SELECT
    k.corp_code,
    k.company_name,
    k.market_cap,
    -- 우선순위 점수: 작을수록 우선
    (
      CASE WHEN k.admin_designated THEN 0 ELSE 100 END +
      CASE WHEN EXISTS (
        SELECT 1 FROM events e
        WHERE e.corp_code = k.corp_code
          AND e.event_type IN ('CB_ISSUANCE','BW_ISSUANCE')
          AND e.event_date > CURRENT_DATE - INTERVAL '12 months'
      ) THEN 0 ELSE 50 END +
      CASE WHEN EXISTS (
        SELECT 1 FROM events e
        WHERE e.corp_code = k.corp_code
          AND e.event_type = 'MAJORITY_HOLDER_CHANGE'
          AND e.event_date > CURRENT_DATE - INTERVAL '12 months'
      ) THEN 0 ELSE 25 END
    ) AS priority_score
  FROM krx_kosdaq k
  WHERE k.market_cap < 50000000000   -- 500억 원 미만
    AND k.trading_status != 'permanently_halted'
    AND k.listed_at < CURRENT_DATE - INTERVAL '6 months'
)
SELECT corp_code, company_name, market_cap
FROM candidates
ORDER BY priority_score ASC, market_cap ASC
LIMIT 100;
```

선정 로직 요약: 관리종목 → CB 발행 이력 → 최대주주변경 이력 → 시총 작은 순.

### 2.2 거래량 spike top 10 (일 1회 + 장중 갱신 선택)

100풀 안에서 매일 장 마감(15:30) 후 거래량 spike 비율 계산.

```
volume_score(corp) =
  ( sum(거래대금, 직전 5거래일) / 5 )
  /
  ( sum(거래대금, 직전 60거래일) / 60 )
```

이 값이 큰 순으로 top 10 선정. 이 10개는 **즉시 알림 대상**이며 누적 신호 점수 가중치를 1.5배 적용한다.

장중 사용 옵션: 장중 12:00에 한 차례 더 계산해 오전 spike를 잡을 수도 있으나, OpenDART rate limit 안에서 v0.1은 장 마감 후 일 1회만 계산.

### 2.3 갱신 조건과 풀 안정성

100풀은 일 1회만 갱신하되, 어제와 오늘의 변화량(churn)을 로깅. churn이 일 평균 ≤ 10건이면 풀이 안정적이라는 신호. churn이 갑자기 커지면 시장 전체 이벤트 가능성 → 알림.

---

## 3. 아키텍처

### 3.1 데이터 흐름

```
[외부 소스]
   DART OpenAPI ──┐
   KRX / pykrx ───┤
   뉴스 · KIND ───┘
                  ↓
    [OCI ARM Ampere A1 단일 VM, 4 OCPU / 24GB RAM]
    ┌───────────────────────────────────────────────┐
    │  수집  →  추출  →  그래프 DB  →  신호 엔진      │
    │ APSched   PDF+NER  PG16+AGE   FastAPI+rules   │
    │  + Redis  + 정합화                              │
    └───────────────┬───────────────────────────────┘
                    ↓
    [출력]
    Telegram Bot 푸시        Telegram Mini App
       (sendMessage)            (HTTPS 정적+API)
```

### 3.2 컨테이너 구성 (docker-compose)

| 서비스 | 이미지 | 역할 |
|---|---|---|
| `postgres` | `apache/age:PG16` | 그래프 + 관계형 단일 DB |
| `redis` | `redis:7-alpine` | 작업 큐, 캐시, rate limit |
| `app` | 자체 빌드 (FastAPI) | API + 워커 + 스케줄러 |
| `bot` | 자체 빌드 (python-telegram-bot) | TG 봇 + 푸시 워커 |
| `caddy` | `caddy:2` | HTTPS 자동 (Let's Encrypt) |

### 3.3 외부 의존성

| 의존성 | 무료 한도 | 비고 |
|---|---|---|
| OpenDART API | 일 10,000건 | v0.1에서 실제 사용량 ≤ 300건/일 |
| Telegram Bot API | 사실상 무제한 | 봇 메시지 30/sec 한도 |
| Claude API (Haiku) | 종량제 | NER 폴백·요약. 일 ≤ 500 콜 예상 |
| OCI Object Storage | 20GB | PDF 아카이브·백업 |
| pykrx (KRX 데이터) | 무료, IP 한도 있음 | 캐시 적극 활용 |

---

## 4. 컴포넌트 명세

### 4.1 수집층 (`app/ingest/`)

| 모듈 | 스케줄 | 책임 |
|---|---|---|
| `universe.py` | 08:30 KST 일 1회 | KRX에서 코스닥 시총·관리종목 정보 받아 universe 갱신 |
| `volume_rank.py` | 15:35 KST 일 1회 | 100풀 5d/60d 거래대금 ratio 계산, watchlist_top10 갱신 |
| `dart_poller.py` | 09:00~18:00 5분 간격 | OpenDART `list.json` 폴링, 100풀 corp_code 필터 |
| `news_crawler.py` (선택) | 30분 간격 | 100풀 회사명으로 NAVER 뉴스 검색 (선택 기능) |

DART 폴링은 `bgn_de=오늘`, `end_de=오늘`로 호출하고 `corp_code` 무필터로 받은 뒤 앱에서 100풀로 필터. 이 방식이 API 호출 수가 가장 적다.

### 4.2 추출층 (`app/extract/`)

| 모듈 | 책임 |
|---|---|
| `struct_fields.py` | OpenDartReader로 임원·CB·최대주주 등 구조화 필드 추출. 1순위. |
| `pdf_parser.py` | 구조화로 잡히지 않는 본문은 `pdfplumber`로 텍스트 추출, OCR 폴백은 `tesseract` (kor) |
| `ner.py` | `Kiwi` 형태소 분석 → 인명/법인명 후보 추출 → 모호한 케이스는 Claude Haiku 1회 호출로 검증 |
| `entity_resolver.py` | corp_code 기반 법인 정합화, 자연인은 (이름, 생년힌트, 등기 회사 set)으로 hash 키 생성, ≥ 0.85 신뢰도면 자동 병합, 미만은 review queue |

자연인 정합화는 본 시스템의 **가장 어려운 부분**이다. 동명이인 분리가 실패하면 그래프 신뢰도 전체가 무너진다. 다음 안전장치를 둔다.

1. 자동 병합 임계치: alias 매칭 + 등기 회사 set 자카드 ≥ 0.5 + 시간적 연속성
2. 임계치 미만 → DB에 분리된 자연인 노드로 유지 + admin review queue
3. 한 번 병합되면 unique 식별자 발급 (`person_uid`)
4. 모든 자연인 노드 표시 시 "동명이인 가능성 X" 플래그 노출

### 4.3 그래프 저장 (`app/graph/`)

PostgreSQL 16 + Apache AGE. AGE는 openCypher 쿼리를 SQL과 동일 트랜잭션에서 실행 가능하다.

| 모듈 | 책임 |
|---|---|
| `schema.sql` | PG 테이블 + AGE 그래프 초기화 |
| `upsert.py` | 노드·엣지 upsert helper |
| `queries.py` | 자주 쓰는 Cypher 쿼리 (예: 자연인의 N-hop 회사 조회) |

### 4.4 신호 엔진 (`app/signals/`)

| 모듈 | 책임 |
|---|---|
| `rules.py` | 룰 정의. 데코레이터 기반 등록 |
| `scorer.py` | 룰 가중합, watchlist top 10 가중치 1.5배 |
| `backtest.py` | KIND 상폐 표본 대비 정밀도·재현율 계산 |

### 4.5 텔레그램 봇 (`bot/`)

| 모듈 | 책임 |
|---|---|
| `handlers.py` | `/start`, `/help`, `/subscribe`, `/unsubscribe`, `/me` 핸들러 |
| `push_worker.py` | 신호 발화 → 구독자에게 메시지 발송. RQ로 비동기 처리 |
| `auth.py` | initData 검증 (HMAC SHA256, Telegram 공식 알고리즘) |

### 4.6 미니앱 프론트엔드 (`web/`)

| 항목 | 값 |
|---|---|
| 프레임워크 | React + Vite |
| SDK | `@telegram-apps/sdk-react` |
| 상태관리 | TanStack Query + Zustand |
| 그래프 시각화 | Cytoscape.js (또는 vis-network) |
| 빌드 결과물 | `web/dist/` → Caddy 정적 서빙 |

---

## 5. 데이터 모델

### 5.1 그래프 스키마 (Apache AGE)

```cypher
// 노드
(:Person {person_uid, name, aliases, birth_year_hint, confidence})
(:Corp {corp_code, name, market, market_cap, listed_at, delisted_at, watchlist_flag, admin_flag})
(:Fund {fund_uid, name, fund_type})   // 신기술조합, 투자조합, SPC
(:Filing {rcept_no, type, filed_at, source_url})

// 엣지
(:Person)-[:DIRECTOR_OF {role, since, until, source_rcept_no}]->(:Corp)
(:Person)-[:LARGEST_HOLDER_OF {pct, since, until}]->(:Corp)
(:Corp)-[:ISSUED_CB {face_amt, rate, conv_price, refixings:int, rcept_no}]->(:Filing)
(:Fund|:Corp|:Person)-[:ACQUIRED_CB_OF {face_amt, at, rcept_no}]->(:Corp)
(:Person)-[:CONTROLS]->(:Fund|:Corp)
(:Filing)-[:MENTIONS]->(:Person|:Corp|:Fund)
```

### 5.2 관계형 스키마 (PG)

```sql
-- 일일 유니버스
CREATE TABLE universe (
  as_of_date DATE NOT NULL,
  corp_code VARCHAR(8) NOT NULL,
  company_name VARCHAR(200),
  market_cap BIGINT,
  priority_score INT,
  PRIMARY KEY (as_of_date, corp_code)
);

-- 일일 watchlist (거래량 spike 10)
CREATE TABLE watchlist_top10 (
  as_of_date DATE NOT NULL,
  corp_code VARCHAR(8) NOT NULL,
  volume_score NUMERIC(10,4),
  rank SMALLINT,
  PRIMARY KEY (as_of_date, corp_code)
);

-- 공시 메타
CREATE TABLE filings (
  rcept_no VARCHAR(14) PRIMARY KEY,
  corp_code VARCHAR(8) NOT NULL,
  filing_type VARCHAR(50),
  filed_at TIMESTAMPTZ,
  source_url TEXT,
  processed_at TIMESTAMPTZ,
  raw_pdf_object_key TEXT
);

-- 추출 이벤트
CREATE TABLE events (
  event_id BIGSERIAL PRIMARY KEY,
  corp_code VARCHAR(8) NOT NULL,
  event_type VARCHAR(50),
  event_date DATE,
  source_rcept_no VARCHAR(14),
  payload JSONB
);

-- 신호 발화
CREATE TABLE signals (
  signal_id BIGSERIAL PRIMARY KEY,
  corp_code VARCHAR(8) NOT NULL,
  rule_name VARCHAR(80),
  score NUMERIC(4,3),
  fired_at TIMESTAMPTZ,
  payload JSONB
);

-- 사용자
CREATE TABLE users (
  user_id BIGSERIAL PRIMARY KEY,
  telegram_user_id BIGINT UNIQUE NOT NULL,
  email VARCHAR(200) UNIQUE,
  media_org VARCHAR(200),
  domain VARCHAR(100),
  status VARCHAR(20) DEFAULT 'pending',  -- pending/approved/rejected/banned
  approved_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 구독 (옵션, v0.1은 all-or-nothing)
CREATE TABLE subscriptions (
  user_id BIGINT NOT NULL REFERENCES users(user_id),
  corp_code VARCHAR(8),   -- NULL이면 전체
  PRIMARY KEY (user_id, corp_code)
);

CREATE INDEX idx_filings_corp ON filings(corp_code, filed_at DESC);
CREATE INDEX idx_events_corp_date ON events(corp_code, event_date DESC);
CREATE INDEX idx_signals_fired ON signals(fired_at DESC);
```

---

## 6. 신호 룰 엔진

### 6.1 룰 정의 예시

```python
# app/signals/rules.py
from .registry import rule
from .events import events_in_window, recent_directors

@rule(name="MA_CB_NEW_BIZ_180D", weight=0.85,
      description="최대주주변경 + CB 발행 + 사명변경/신사업 추가가 180일 내 모두 발생")
def majority_change_plus_cb_plus_pivot(corp, days=180):
    e = events_in_window(corp, days)
    has_ma = any(x.type == "MAJORITY_HOLDER_CHANGE" for x in e)
    has_cb = any(x.type in ("CB_ISSUANCE", "BW_ISSUANCE") for x in e)
    has_pivot = any(x.type in ("PURPOSE_ADDITION", "CORP_NAME_CHANGE") for x in e)
    return has_ma and has_cb and has_pivot

@rule(name="REPEAT_DIRECTOR_DISTRESSED", weight=0.70,
      description="신규 등기임원이 직전 5년 ≥ 2개 한계기업 등기 이력 보유")
def director_history_in_distressed(corp):
    new_dirs = recent_directors(corp, days=180)
    for p in new_dirs:
        past = graph_query(
            "MATCH (p:Person {person_uid:$uid})-[:DIRECTOR_OF]->(c:Corp) "
            "WHERE c.delisted_at IS NOT NULL OR c.admin_flag = true "
            "RETURN count(c) AS n",
            uid=p.person_uid
        )
        if past[0]["n"] >= 2:
            return True
    return False

@rule(name="CB_REFIX_CHAIN", weight=0.60,
      description="365일 내 CB 전환가액 하향 조정 ≥ 2회")
def cb_refixing_chain(corp, days=365):
    return count_events(corp, "CB_REFIX_DOWN", days) >= 2

@rule(name="CB_ACQUIRER_RECURRENCE", weight=0.75,
      description="신규 CB 인수자(또는 실질지배자)가 다른 한계기업 CB 인수 이력 보유")
def cb_acquirer_recurrence(corp):
    recent_cb_acquirers = get_recent_cb_acquirers(corp, days=180)
    for a in recent_cb_acquirers:
        past = graph_query(
            "MATCH (a)-[:ACQUIRED_CB_OF]->(c:Corp) "
            "WHERE id(a)=$id AND c.delisted_at IS NOT NULL "
            "RETURN count(c) AS n",
            id=a.node_id
        )
        if past[0]["n"] >= 1:
            return True
    return False

@rule(name="AUDITOR_CHANGE_PLUS_QUALIFIED", weight=0.55,
      description="감사인 변경 후 직전기 한정·거절 의견")
def auditor_change_qualified(corp):
    return (has_event(corp, "AUDITOR_CHANGE", days=400)
            and has_event(corp, "AUDIT_OPINION_QUALIFIED", days=400))
```

### 6.2 점수 합산

```python
def compute_score(corp):
    score = 0.0
    fired_rules = []
    for rule in registry.all():
        if rule.check(corp):
            score += rule.weight
            fired_rules.append(rule.name)

    # watchlist top 10이면 1.5배 가중
    if is_in_watchlist_top10(corp):
        score *= 1.5

    return min(score, 1.0), fired_rules
```

### 6.3 알림 트리거

| 점수 구간 | 행동 |
|---|---|
| < 0.5 | 누적 기록만, 알림 없음 |
| 0.5 ~ 0.7 | 일일 리포트에만 포함 |
| ≥ 0.7 | 즉시 푸시 + 일일 리포트 |
| ≥ 0.9 | 즉시 푸시 + 미니앱 push notification + admin email 사본 |

---

## 7. API 사양

REST/JSON. 모든 엔드포인트는 `/api/v1` 프리픽스. Telegram initData 인증 헤더(`X-Telegram-Init-Data`) 필수 (`/auth/*` 제외).

```
POST /api/v1/auth/email/request    # 이메일 인증 코드 발송
  body: { email }
  resp: { request_id, expires_in_sec }

POST /api/v1/auth/email/verify     # 코드 입력
  body: { request_id, code }
  resp: { status: "approved"|"review_queued", user }

GET  /api/v1/me                    # 내 정보
GET  /api/v1/universe              # 오늘의 100풀
GET  /api/v1/watchlist             # 오늘의 top 10
GET  /api/v1/corp/{code}           # 종목 상세 (재무, 시총, 관리종목 여부)
GET  /api/v1/corp/{code}/timeline  # 공시 타임라인
GET  /api/v1/corp/{code}/graph     # 1-hop 인물·법인 그래프 (Cytoscape JSON)
GET  /api/v1/corp/{code}/signals   # 신호 발화 이력
GET  /api/v1/person/{uid}          # 자연인 상세 (등기 회사 리스트만, 평가 없음)
GET  /api/v1/search?q=...          # 회사명·인명 검색
```

### 응답 예시: 종목 상세

```json
{
  "corp_code": "01234567",
  "company_name": "예시(주)",
  "market_cap": 38000000000,
  "in_universe": true,
  "in_watchlist_top10": true,
  "volume_score": 4.21,
  "admin_designated": false,
  "current_signal_score": 0.78,
  "fired_rules": [
    {"name":"MA_CB_NEW_BIZ_180D","fired_at":"2026-05-10T09:13:00+09:00"},
    {"name":"REPEAT_DIRECTOR_DISTRESSED","fired_at":"2026-05-11T16:22:00+09:00"}
  ],
  "disclaimer": "본 정보는 공시 사실의 색인이며 평가나 투자 권유가 아닙니다."
}
```

---

## 8. 텔레그램 미니앱

### 8.1 봇 셋업 절차

1. `@BotFather` → `/newbot` → 봇 이름 등록
2. `/setdomain` → 미니앱 호스팅 도메인 등록 (HTTPS 필수)
3. `/setmenubutton` → 미니앱 진입 버튼 설정 (URL: `https://yourdomain.com/twa`)
4. `/setdescription`, `/setabouttext`, `/setuserpic` 설정
5. 봇 토큰을 OCI VM의 환경변수 `TELEGRAM_BOT_TOKEN`으로 주입

### 8.2 initData 검증

미니앱이 호출하는 모든 API는 `WebApp.initData`를 검증해야 한다. Telegram 공식 알고리즘:

```python
import hmac, hashlib
from urllib.parse import parse_qsl

def verify_init_data(init_data: str, bot_token: str) -> dict | None:
    parsed = dict(parse_qsl(init_data, strict_parsing=True))
    received_hash = parsed.pop("hash", None)
    if not received_hash:
        return None
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed.items())
    )
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    expected_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(received_hash, expected_hash):
        return None
    return parsed
```

`auth_date`가 24시간 이내인지 추가로 확인.

### 8.3 푸시 알림

봇이 신호 발화 이벤트를 RQ 큐에서 가져와 구독자에게 `sendMessage` 호출. 알림 메시지는 인라인 키보드로 미니앱 deep link 제공.

```python
# bot/push_worker.py
def send_signal_notification(user, signal):
    text = (
        f"⚠️ 신호 발화: {signal.company_name} ({signal.corp_code})\n"
        f"점수: {signal.score:.2f}\n"
        f"발화 룰: {', '.join(signal.fired_rules)}\n\n"
        f"공시 원문과 인물·법인 그래프를 미니앱에서 확인하세요.\n"
        f"※ 본 정보는 공시 사실의 색인이며 평가나 투자 권유가 아닙니다."
    )
    keyboard = {
        "inline_keyboard": [[{
            "text": "미니앱에서 보기",
            "web_app": {"url": f"https://yourdomain.com/twa?corp={signal.corp_code}"}
        }]]
    }
    bot.send_message(
        chat_id=user.telegram_user_id,
        text=text,
        reply_markup=keyboard
    )
```

Rate limit: Telegram은 봇당 30 msg/sec, 같은 chat에는 1 msg/sec. v0.1 사용자 수에서는 문제없음.

---

## 9. 언론사 이메일 검증

### 9.1 가입 플로우

```
[미니앱] 이메일 입력
    ↓
POST /api/v1/auth/email/request
    ↓
서버: 6자리 코드 생성 → Redis 저장 (TTL 10분)
    ↓
이메일 발송 (OCI Email Delivery 또는 SendGrid 무료티어)
    ↓
[미니앱] 코드 입력
    ↓
POST /api/v1/auth/email/verify
    ↓
서버: 코드 검증 → 도메인 화이트리스트 확인
    ↓
화이트리스트 OK → 즉시 승인, users.status = 'approved'
화이트리스트 NG → admin review queue, users.status = 'pending'
                  텔레그램 admin 채널에 알림
```

### 9.2 도메인 화이트리스트 운영

소스: 한국언론진흥재단 등록 언론사 목록 + 자체 큐레이션. JSON 파일로 관리하고 매월 수동 검토.

```json
// data/media_domains.json
{
  "version": "2026-05",
  "updated_at": "2026-05-01",
  "domains": [
    "chosun.com",
    "joongang.co.kr",
    "donga.com",
    "hani.co.kr",
    "khan.co.kr",
    "hankyung.com",
    "mk.co.kr",
    "mt.co.kr",
    "edaily.co.kr",
    "newsis.com",
    "yna.co.kr",
    "ytn.co.kr",
    "sbs.co.kr",
    "kbs.co.kr",
    "mbc.co.kr",
    "...": "총 ~300개"
  ]
}
```

### 9.3 Admin Review

화이트리스트에 없으면 admin review queue. 관리자는 텔레그램 admin 채널에서 승인/거절 버튼 클릭.

```
[Admin Bot 채널 메시지]
🆕 가입 신청
이메일: kim@unknown-media.kr
TG ID: 123456789
사용자명: @reporter_kim
사유: 신규 인터넷 언론사 추정

[승인] [거절]
```

승인 시 도메인을 화이트리스트에 자동 추가 옵션.

### 9.4 약관 동의 의무

가입 시 다음 약관에 명시 동의해야 함.

- 본 서비스는 공시 사실의 색인 및 알림이며, 회사·자연인에 대한 평가가 아님
- 보도 인용 시 출처를 DART 공시 원문으로 표기할 것
- 본 서비스 데이터를 그대로 retail 배포·SNS 게시하지 않을 것
- 위반 시 즉시 사용 정지 가능

---

## 10. OCI Free Tier 배포

### 10.1 자원 배치

| 자원 | 사용 |
|---|---|
| ARM Ampere A1 Flex VM | 4 OCPU / 24GB RAM, Ubuntu 22.04 |
| Block Volume | 200GB (PG 데이터 + Redis AOF) |
| Object Storage | 20GB (PDF 아카이브 + nightly dump) |
| Load Balancer | 10 Mbps Flex (선택, Caddy 자체로도 충분) |
| Email Delivery | 무료 한도 내 (월 ~3,000건) |

### 10.2 docker-compose 골격

```yaml
version: "3.9"
services:
  postgres:
    image: apache/age:PG16_latest
    environment:
      POSTGRES_PASSWORD: ${PG_PASSWORD}
      POSTGRES_DB: dartgraph
    volumes:
      - pg_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

  app:
    build: ./app
    environment:
      DATABASE_URL: postgresql://postgres:${PG_PASSWORD}@postgres/dartgraph
      REDIS_URL: redis://redis:6379/0
      DART_API_KEY: ${DART_API_KEY}
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
      TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN}
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  bot:
    build: ./bot
    environment:
      TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN}
      DATABASE_URL: postgresql://postgres:${PG_PASSWORD}@postgres/dartgraph
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  caddy:
    image: caddy:2
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - ./web/dist:/srv/twa
      - caddy_data:/data
      - caddy_config:/config
    restart: unless-stopped

volumes:
  pg_data:
  redis_data:
  caddy_data:
  caddy_config:
```

### 10.3 Caddyfile

```
yourdomain.com {
    encode gzip

    handle /twa* {
        root * /srv/twa
        try_files {path} /index.html
        file_server
    }

    handle /api/* {
        reverse_proxy app:8000
    }

    handle {
        redir https://yourdomain.com/twa permanent
    }
}
```

### 10.4 프로젝트 구조

```
dart-graph-monitor/
├── docker-compose.yml
├── Caddyfile
├── .env.example
├── alembic/
├── app/
│   ├── main.py                 # FastAPI entrypoint
│   ├── settings.py
│   ├── api/
│   │   ├── auth.py
│   │   ├── universe.py
│   │   ├── corp.py
│   │   └── person.py
│   ├── ingest/
│   │   ├── universe.py
│   │   ├── volume_rank.py
│   │   ├── dart_poller.py
│   │   └── news_crawler.py
│   ├── extract/
│   │   ├── struct_fields.py
│   │   ├── pdf_parser.py
│   │   ├── ner.py
│   │   └── entity_resolver.py
│   ├── graph/
│   │   ├── schema.sql
│   │   ├── upsert.py
│   │   └── queries.py
│   ├── signals/
│   │   ├── registry.py
│   │   ├── rules.py
│   │   ├── scorer.py
│   │   └── backtest.py
│   ├── workers/
│   │   └── tasks.py            # RQ 잡
│   └── scheduler.py            # APScheduler
├── bot/
│   ├── main.py
│   ├── handlers.py
│   ├── auth.py
│   ├── push_worker.py
│   └── admin.py
├── web/                        # Telegram Mini App (React + Vite)
│   ├── package.json
│   ├── vite.config.ts
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── pages/
│   │   │   ├── Onboarding.tsx
│   │   │   ├── Watchlist.tsx
│   │   │   ├── CorpDetail.tsx
│   │   │   └── PersonDetail.tsx
│   │   ├── components/
│   │   │   └── EntityGraph.tsx  # Cytoscape wrapper
│   │   └── api/
│   │       └── client.ts
│   └── dist/                   # 빌드 결과물
├── data/
│   └── media_domains.json
├── tests/
│   └── backtest/
│       └── delisting_panel.py
└── infra/
    ├── terraform/
    └── ansible/
```

---

## 11. 운영

### 11.1 로그

- 모든 서비스 stdout → `docker logs`
- 오류는 자체 Telegram admin 채널로도 푸시
- 일별 통계 (공시 수집 수, 추출 성공률, 신호 발화 수) 18:00 KST에 admin 채널 자동 전송

### 11.2 모니터링

- Uptime Kuma (셀프호스트, 작은 컨테이너) — 헬스체크
- `/healthz` 엔드포인트 — DB·Redis·DART 응답 확인

### 11.3 백업

```bash
# 매일 03:00 KST
0 3 * * * docker exec postgres pg_dump dartgraph | gzip > /backup/$(date +\%Y\%m\%d).sql.gz
# OCI CLI로 Object Storage 업로드
oci os object put --bucket-name dartgraph-backup --file /backup/$(date +%Y%m%d).sql.gz
# 14일 retention
find /backup -mtime +14 -delete
```

### 11.4 Rate Limit

- OpenDART: 자체 토큰 버킷 (8 req/sec, 일 10,000) — `tenacity` 백오프
- Telegram Bot: `python-telegram-bot`의 내장 rate limiter 활성화
- Claude API: 일별 한도 환경변수로 제어

---

## 12. 법적·윤리 가드레일 (재강조)

1. **사실 색인 원칙**: 모든 출력에 "공시 사실의 색인이며 평가나 투자 권유가 아님" 워터마크
2. **자연인 노드 표시**: 항상 DART rcept_no 백링크 + "동명이인 가능성" 플래그
3. **자동 점수는 종목 단위만**: 자연인 단위 점수 표시 금지
4. **언론사 가입 자격 제한**: 등록 도메인 검증 + 약관 동의
5. **사용자 약관**: retail 그대로 배포·SNS 게시 금지 명시
6. **데이터 보존 정책**: 자연인 노드는 신뢰도 미달 시 자동 삭제 룰 운영
7. **공식 reply**: 회사 또는 자연인이 사실 정정 요청 시 ≤ 72시간 내 처리 프로세스

---

## 13. 로드맵

### v0.1 (2~3주) — 검증 단계

- 종목 유니버스 100개 갱신
- DART 폴링 + 구조화 필드 추출
- 룰 5개 + 가중합 스코어
- 텔레그램 봇 알림
- KIND 표본 50건으로 백테스트

### v0.2 (4~6주) — 미니앱

- 미니앱 SPA
- 가입 플로우 (언론사 이메일 검증)
- 종목 상세 페이지
- 인물·법인 그래프 뷰 (Cytoscape)

### v0.3 (8~10주) — 정밀도 향상

- PDF/OCR 폴백
- 자연인 entity resolution 정밀도 ≥ 0.9
- 백테스트 표본 200건으로 확대
- 룰 8~12개

### v0.4 (3~4개월) — 외부 데이터 통합

- NAVER 뉴스 cross-reference
- 법원 등기 등기변동 데이터
- 신용평가사·기관 데이터 (유료)
- 영문 베타 (해외 매체)

### v1.0 (6개월) — 정식 운영

- B2B 채널 (증권사 컴플라이언스, VC 실사) 베타
- 한정된 retail 베타 (기관 추천제)

---

## 부록 A. 환경 변수

```
DATABASE_URL=postgresql://postgres:pw@postgres/dartgraph
REDIS_URL=redis://redis:6379/0
DART_API_KEY=...
ANTHROPIC_API_KEY=sk-ant-...
TELEGRAM_BOT_TOKEN=123456:ABC...
TELEGRAM_ADMIN_CHAT_ID=-100...
EMAIL_FROM=no-reply@yourdomain.com
EMAIL_SMTP_HOST=...
EMAIL_SMTP_USER=...
EMAIL_SMTP_PASSWORD=...
HOST_DOMAIN=yourdomain.com
SIGNAL_THRESHOLD_NOTIFY=0.7
SIGNAL_THRESHOLD_CRITICAL=0.9
```

## 부록 B. 초기 셋업 명령

```bash
# OCI VM 접속 후
sudo apt update && sudo apt install -y docker.io docker-compose-plugin git
git clone https://github.com/yourorg/dart-graph-monitor.git
cd dart-graph-monitor
cp .env.example .env
# .env 편집
docker compose up -d postgres redis
docker compose exec postgres psql -U postgres -d dartgraph -f /docker-entrypoint-initdb.d/schema.sql
docker compose exec postgres psql -U postgres -d dartgraph -c "LOAD 'age'; SELECT create_graph('relations');"
docker compose up -d
```
