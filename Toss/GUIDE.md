# 사용 설명서 — Toss × AMQS 퀀트 대시보드

> 설치 · 실행 · 토스 Open API 연동 · 서버 API · 종목 교체 가이드.
> **전략 철학과 주의점은 [README.md](./README.md)를 먼저 읽어 주세요.**

> 토스증권 **Open API**로 국내 주식·ETF 시세를 받아,
> **Adaptive Momentum Quant Strategy (AMQS)** 룰을 기계적으로 적용해
> **매수 / 보유 / 매도** 시그널을 보여주는 웹 대시보드.

한국인이 선호하는 **섹터별 대표주(섹터당 10종목)** 와 **인기 ETF 10종목** 을 한 화면에 띄우고,
종목명·코드로 **직접 검색** 해 동일한 방식으로 시그널을 확인할 수 있습니다.

`npm start` 후 브라우저에서 바로 확인할 수 있습니다 — 상단 레짐 배너, ETF 그리드,
섹터별 카드(매수=초록 / 보유=노랑 / 매도=빨강 테두리), 검색 결과 패널로 구성됩니다.

---

## 무엇을 보여주나

- **시장 레짐 배너** — KODEX 200(KOSPI200 프록시)의 200일선·5일 수익률·변동성으로 시장 국면 판정
  - `위험 선호(RISK_ON)` / `위험 회피(RISK_OFF)` / `방어(DEFENSIVE)`
- **ETF 10종목** — 개인투자자 선호 ETF(KODEX 200, TIGER 미국S&P500/나스닥100/필반 등)에 시그널 표시
- **섹터별 대표주 8섹터 × 10종목** — 반도체/AI · 2차전지 · 자동차 · 인터넷/게임 · 바이오 · 방산/조선 · 금융 · 엔터
- **종목 검색** — 종목명 또는 6자리 코드를 입력하면 모멘텀 점수·손절선·근거와 함께 시그널 출력

각 종목 카드에는 모멘텀 점수(0~100), 12-1·6-1 모멘텀, 60일 변동성, 손절선, 시그널 **근거**가 표시됩니다.

---

## AMQS 시그널 룰 (요약)

원본 전략: [`01.Trading Strategy/Adaptive Momentum Quant Strategy (AMQS)`](../01.Trading%20Strategy/Adaptive%20Momentum%20Quant%20Strategy%20(AMQS)/readme.md)

**4-Factor Composite 모멘텀** (universe 내 횡단면 z-score):

```
score = 0.50·Z(12-1) + 0.30·Z(6-1) + 0.15·Z(3-1) + 0.05·Z(1/Vol)
```

- `12-1` = 12개월 전 → 1개월 전 수익률 (최근 1개월 제외 = 단기 평균회귀 차단)
- `Vol` = 60일 실현 변동성(연환산)

**종목별 시그널 판정:**

| 조건 | 시그널 |
| --- | --- |
| 60일 고점 대비 −12% 이탈 (트레일링 스탑) | **매도(SELL)** |
| composite z ≥ +0.5 (상위권) | **매수(BUY)** |
| composite z ≤ −0.5 (하위권, 추세 약화) | **매도(SELL)** |
| 그 외 | **보유(HOLD)** |

**레짐 오버레이:**

- `방어(DEFENSIVE)` — 신규 매수 보류, 매수 후보는 **회피(AVOID)** 처리
- `위험 회피(RISK_OFF)` — 매수 강도 하향 → 보유로 다운그레이드

### 원본 대비 국내 적용 변경점

| 항목 | 원본(미국) | 본 대시보드(국내) |
| --- | --- | --- |
| 레짐 벤치마크 | QQQ 200일선 | **KODEX 200** 200일선 |
| 공포지수 | VIX | KODEX 200 **20일 실현 변동성**(>30% 시 위험회피) |
| 가중치·룩백·손절 | 동일 | **동일** |

> VIX에 직접 대응하는 국내 지수(VKOSPI)는 본 Open API 스펙에 없어 실현 변동성으로 대체했습니다.

---

## 빠른 시작

```bash
cd Toss
npm install
npm start            # http://localhost:3000
```

### 토스증권 Open API 연동 (실데이터)

자격증명이 **없으면 MOCK 모드**(결정론적 시연 데이터)로 즉시 실행됩니다.
실데이터를 쓰려면 [developers.tossinvest.com](https://developers.tossinvest.com/docs)에서
앱을 등록해 `client_id` / `client_secret` 을 발급받아 `.env` 에 넣으세요.

```bash
cp .env.example .env
# .env 편집:
# TOSS_CLIENT_ID=발급받은_아이디
# TOSS_CLIENT_SECRET=발급받은_시크릿
npm start            # 상단 'MOCK 모드' 배너가 사라지면 실데이터
```

> `.env` 는 의존성 없이 서버가 직접 로드합니다(`dotenv` 불필요). `.env` 는 `.gitignore` 에 포함되어 있습니다.

사용 엔드포인트(토스 Open API):

- `POST /oauth2/token` — OAuth2 Client Credentials, 토큰 캐싱
- `GET /api/v1/candles?symbol=&interval=1d&count=200` — 일봉(필요 시 `before` 페이지네이션)
- `GET /api/v1/prices?symbols=` — 현재가

---

## 서버 API

| 메서드 | 경로 | 설명 |
| --- | --- | --- |
| GET | `/api/health` | 모드(MOCK/LIVE)·섹터/ETF 개수 |
| GET | `/api/dashboard` | 레짐 + 섹터별 종목 + ETF 시그널(5분 캐시) |
| GET | `/api/search?q=` | 종목명/6자리 코드 검색 후 시그널 |

**공유 가능한 검색 링크**: 브라우저에서 `http://localhost:3000/?q=삼성전자` 처럼 `?q=` 를 붙이면
해당 종목 검색 결과가 자동으로 펼쳐집니다(공유·북마크용).

---

## 종목 교체

[`src/universe.js`](./src/universe.js) 의 `SECTORS` / `ETFS` 배열에서 `{ code, name }` 만 바꾸면
엔진·프론트엔드는 그대로 동작합니다. 종목코드는 KRX 6자리 표준코드를 사용합니다.

---

## 한계 및 주의

- **투자 권유가 아닙니다.** AMQS 룰을 기계적으로 적용한 정보일 뿐이며, 모든 투자 책임은 본인에게 있습니다.
- 모멘텀 전략은 **추세 전환점에서 단기 −15~30% 손실** 가능성이 있습니다(원본 README의 "모멘텀 크래시 위험" 참조).
- 토스 Open API 일봉은 요청당 최대 200개입니다. 12개월 모멘텀(약 252거래일)은 `before` 페이지네이션으로 보충합니다.
- 섹터/ETF 구성은 2026년 기준 개인 선호·증권사 톱픽을 참고한 **예시 큐레이션** 이며, 시장 변화에 맞게 교체하세요.
- MOCK 데이터는 종목코드 해시 기반 합성 시계열이라 **실제 가격과 무관** 합니다(배너로 표시). 가격대·시그널 분포 확인용입니다.

---

**전략 원작자**: 김호광 (Dennis Kim) · [vibe-investing](https://github.com/gameworkerkim/vibe-investing) · MIT License
