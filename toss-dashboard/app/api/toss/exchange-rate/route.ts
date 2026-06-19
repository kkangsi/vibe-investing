import { NextResponse } from "next/server";
import { getExchangeRate, isMockMode } from "@/lib/toss";
import { cacheGet, cacheSet, CACHE_KEYS } from "@/lib/redis";

export async function GET() {
  const cacheKey = CACHE_KEYS.exchangeRate();
  const cached = await cacheGet(cacheKey);
  if (cached) {
    return NextResponse.json({ data: cached, cached: true });
  }

  if (isMockMode()) {
    const mock = { rate: 1380, updatedAt: new Date().toISOString() };
    return NextResponse.json({ data: mock, mock: true });
  }

  try {
    const rate = await getExchangeRate();
    await cacheSet(cacheKey, rate, 60); // 1분 캐시
    return NextResponse.json({ data: rate });
  } catch {
    return NextResponse.json({ data: { rate: 1380, updatedAt: new Date().toISOString() }, mock: true });
  }
}
