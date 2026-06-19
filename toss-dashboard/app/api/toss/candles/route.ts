import { NextRequest, NextResponse } from "next/server";
import { getCandles, generateMockCandles, isMockMode } from "@/lib/toss";
import { cacheGet, cacheSet, CACHE_KEYS } from "@/lib/redis";

export async function GET(req: NextRequest) {
  const symbol = req.nextUrl.searchParams.get("symbol");
  const count = Number(req.nextUrl.searchParams.get("count") ?? "60");

  if (!symbol) {
    return NextResponse.json({ error: "symbol 파라미터가 필요합니다." }, { status: 400 });
  }

  const cacheKey = CACHE_KEYS.candles(symbol);
  const cached = await cacheGet(cacheKey);
  if (cached) {
    return NextResponse.json({ data: cached, cached: true });
  }

  let candles;
  if (isMockMode()) {
    candles = generateMockCandles(symbol, count);
  } else {
    try {
      candles = await getCandles(symbol, count);
    } catch {
      candles = generateMockCandles(symbol, count);
    }
  }

  await cacheSet(cacheKey, candles, 300); // 5분 캐시
  return NextResponse.json({ data: candles, mock: isMockMode() });
}
