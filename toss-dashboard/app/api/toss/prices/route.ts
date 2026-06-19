import { NextRequest, NextResponse } from "next/server";
import {
  getPrices,
  generateMockPrices,
  isMockMode,
} from "@/lib/toss";
import { cacheGet, cacheSet, CACHE_KEYS } from "@/lib/redis";
import {
  POPULAR_KR_STOCKS,
  POPULAR_KR_ETFS,
  KR_SECTORS,
  US_STOCKS,
  US_ETFS,
  findStock,
} from "@/lib/universe";
import type { DashboardStock } from "@/types/toss";

function getSymbolsForTab(tab: string): string[] {
  switch (tab) {
    case "popular":
      return [
        ...POPULAR_KR_STOCKS.map((s) => s.symbol),
        ...POPULAR_KR_ETFS.map((s) => s.symbol),
      ];
    case "kr":
      return KR_SECTORS.flatMap((sec) => sec.stocks.map((s) => s.symbol));
    case "us":
      return [
        ...US_STOCKS.map((s) => s.symbol),
        ...US_ETFS.map((s) => s.symbol),
      ];
    default:
      return [];
  }
}

export async function GET(req: NextRequest) {
  const tab = req.nextUrl.searchParams.get("tab") ?? "popular";
  const cacheKey = CACHE_KEYS.prices(tab);

  // Redis 캐시 확인 (30초 TTL)
  const cached = await cacheGet<DashboardStock[]>(cacheKey);
  if (cached) {
    return NextResponse.json({ data: cached, cached: true });
  }

  const symbols = getSymbolsForTab(tab);

  let prices;
  if (isMockMode()) {
    prices = generateMockPrices(symbols);
  } else {
    try {
      prices = await getPrices(symbols);
    } catch (err) {
      console.error("Toss API 오류, mock 전환:", err);
      prices = generateMockPrices(symbols);
    }
  }

  const result: DashboardStock[] = prices.map((p) => {
    const info = findStock(p.symbol);
    return {
      ...p,
      name: info?.name ?? p.symbol,
      nameKr: info?.nameKr,
      market: info?.market ?? (p.currency === "USD" ? "US" : "KR"),
      sector: info?.sector,
      tag: info?.tag,
    };
  });

  await cacheSet(cacheKey, result, 30);
  return NextResponse.json({ data: result, cached: false, mock: isMockMode() });
}
