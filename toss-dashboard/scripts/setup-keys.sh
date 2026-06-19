#!/bin/bash

ENV_FILE="$(dirname "$0")/../.env.local"

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║        TOSS x Vibe Invest — API 키 설정       ║"
echo "╚══════════════════════════════════════════════╝"
echo ""
echo "토스증권 PC 웹사이트에서 발급한 키를 입력하세요."
echo "→ https://tossinvest.com (로그인 후 개발자 설정)"
echo ""

# ── Toss API ──────────────────────────────────────
read -p "TOSS_CLIENT_ID     : " TOSS_CLIENT_ID
read -s -p "TOSS_CLIENT_SECRET : " TOSS_CLIENT_SECRET
echo ""

# ── Neon PostgreSQL (선택) ─────────────────────────
echo ""
echo "── Neon PostgreSQL (선택, 없으면 Enter 스킵) ──"
echo "→ https://neon.tech"
read -p "DATABASE_URL       : " DATABASE_URL

# ── Upstash Redis (선택) ──────────────────────────
echo ""
echo "── Upstash Redis (선택, 없으면 Enter 스킵) ──"
echo "→ https://console.upstash.com"
read -p "UPSTASH_REDIS_REST_URL   : " UPSTASH_REDIS_REST_URL
read -s -p "UPSTASH_REDIS_REST_TOKEN : " UPSTASH_REDIS_REST_TOKEN
echo ""

# ── 검증 ─────────────────────────────────────────
if [[ -z "$TOSS_CLIENT_ID" || -z "$TOSS_CLIENT_SECRET" ]]; then
  echo ""
  echo "❌ TOSS_CLIENT_ID 또는 TOSS_CLIENT_SECRET이 비어있습니다. 종료합니다."
  exit 1
fi

# ── .env.local 작성 ───────────────────────────────
cat > "$ENV_FILE" <<EOF
# Toss Securities Open API
TOSS_CLIENT_ID=${TOSS_CLIENT_ID}
TOSS_CLIENT_SECRET=${TOSS_CLIENT_SECRET}

# Neon PostgreSQL
DATABASE_URL=${DATABASE_URL}

# Upstash Redis
UPSTASH_REDIS_REST_URL=${UPSTASH_REDIS_REST_URL}
UPSTASH_REDIS_REST_TOKEN=${UPSTASH_REDIS_REST_TOKEN}
EOF

echo ""
echo "✅ .env.local 저장 완료"

# ── 토큰 발급 테스트 ──────────────────────────────
echo ""
echo "🔑 토스 API 토큰 발급 테스트 중..."

RESPONSE=$(curl -s -X POST "https://openapi.tossinvest.com/oauth2/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=${TOSS_CLIENT_ID}&client_secret=${TOSS_CLIENT_SECRET}")

if echo "$RESPONSE" | grep -q "access_token"; then
  echo "✅ 토큰 발급 성공 — 실시간 데이터 모드로 실행됩니다"
  echo ""
  echo "▶  서버 시작: npm run dev"
  echo "▶  접속 주소: http://localhost:3002"
else
  echo "⚠️  토큰 발급 실패 (MOCK MODE로 실행됩니다)"
  echo "   응답: $RESPONSE"
  echo ""
  echo "   키를 다시 확인하거나 토스증권 사전 신청 상태를 확인하세요."
  echo "   → https://tossinvest.com"
fi

echo ""
