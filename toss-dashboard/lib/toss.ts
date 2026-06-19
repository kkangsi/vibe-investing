import type { TossToken, StockPrice, Candle, ExchangeRate } from "@/types/toss";

const BASE_URL = "https://openapi.tossinvest.com";

let cachedToken: TossToken | null = null;

async function getToken(): Promise<string> {
  const clientId = process.env.TOSS_CLIENT_ID;
  const clientSecret = process.env.TOSS_CLIENT_SECRET;

  if (!clientId || !clientSecret) {
    throw new Error("TOSS_CLIENT_ID / TOSS_CLIENT_SECRET 환경변수가 없습니다.");
  }

  const now = Date.now() / 1000;
  if (cachedToken && now < cachedToken.issued_at + cachedToken.expires_in - 3600) {
    return cachedToken.access_token;
  }

  const res = await fetch(`${BASE_URL}/oauth2/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "client_credentials",
      client_id: clientId,
      client_secret: clientSecret,
    }),
    cache: "no-store",
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`토큰 발급 실패 (${res.status}): ${text}`);
  }

  const data = await res.json();
  cachedToken = { ...data, issued_at: now };
  return cachedToken!.access_token;
}

async function tossGet(path: string, params?: Record<string, string>) {
  const token = await getToken();
  const url = new URL(`${BASE_URL}${path}`);
  if (params) {
    Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));
  }

  const res = await fetch(url.toString(), {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store",
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Toss API 오류 (${res.status}) ${path}: ${text}`);
  }

  return res.json();
}

// 현재가 배치 조회 — result[].lastPrice (string)
async function fetchPrices(symbols: string[]): Promise<Record<string, number>> {
  const data = await tossGet("/api/v1/prices", { symbols: symbols.join(",") });
  const items: Array<{ symbol: string; lastPrice: string }> = data.result ?? [];
  const map: Record<string, number> = {};
  for (const item of items) {
    map[item.symbol] = parseFloat(item.lastPrice) || 0;
  }
  return map;
}

// 캔들 조회 — result.candles[].closePrice (string)
export async function getCandles(symbol: string, count = 60): Promise<Candle[]> {
  const data = await tossGet("/api/v1/candles", {
    symbol,
    interval: "1d",
    count: String(Math.min(count, 200)),
  });

  const items: Array<{
    timestamp: string;
    openPrice: string;
    highPrice: string;
    lowPrice: string;
    closePrice: string;
    volume: string;
  }> = data.result?.candles ?? [];

  return items.map((c) => ({
    time: c.timestamp.split("T")[0],
    open: parseFloat(c.openPrice) || 0,
    high: parseFloat(c.highPrice) || 0,
    low: parseFloat(c.lowPrice) || 0,
    close: parseFloat(c.closePrice) || 0,
    volume: parseInt(c.volume) || 0,
  }));
}

// 전일 종가 조회용 캔들 (2일치)
async function fetchPrevClose(symbol: string): Promise<number> {
  try {
    const data = await tossGet("/api/v1/candles", {
      symbol,
      interval: "1d",
      count: "2",
    });
    const candles: Array<{ closePrice: string }> = data.result?.candles ?? [];
    // candles[0] = 오늘, candles[1] = 전일
    if (candles.length >= 2) return parseFloat(candles[1].closePrice) || 0;
    if (candles.length === 1) return parseFloat(candles[0].closePrice) || 0;
    return 0;
  } catch {
    return 0;
  }
}

// concurrency 제한 병렬 실행
async function parallel<T>(
  tasks: (() => Promise<T>)[],
  concurrency = 8
): Promise<T[]> {
  const results: T[] = new Array(tasks.length);
  let idx = 0;

  async function worker() {
    while (idx < tasks.length) {
      const i = idx++;
      results[i] = await tasks[i]();
    }
  }

  const workers = Array.from({ length: Math.min(concurrency, tasks.length) }, worker);
  await Promise.all(workers);
  return results;
}

// 현재가 + 변동률 통합 조회
export async function getPrices(symbols: string[]): Promise<StockPrice[]> {
  if (symbols.length === 0) return [];

  // 1) 현재가 배치 조회
  const batches: string[][] = [];
  for (let i = 0; i < symbols.length; i += 200) {
    batches.push(symbols.slice(i, i + 200));
  }
  const priceMaps = await Promise.all(batches.map(fetchPrices));
  const priceMap: Record<string, number> = Object.assign({}, ...priceMaps);

  // 2) 전일 종가 병렬 조회 (concurrency=8)
  const prevCloses = await parallel(
    symbols.map((sym) => () => fetchPrevClose(sym)),
    8
  );

  // 3) 변동률 계산
  return symbols.map((symbol, i) => {
    const price = priceMap[symbol] ?? 0;
    const prev = prevCloses[i] ?? 0;
    const change = prev > 0 ? price - prev : 0;
    const changeRate = prev > 0 ? (change / prev) * 100 : 0;
    const isUS = /^[A-Z]{1,5}$/.test(symbol);

    return {
      symbol,
      price,
      change,
      changeRate,
      volume: 0, // prices API에 volume 없음 — 필요시 candle에서 추출
      currency: isUS ? "USD" : "KRW",
    };
  });
}

// 환율 조회
export async function getExchangeRate(): Promise<ExchangeRate> {
  const data = await tossGet("/api/v1/exchange-rate");
  // 실제 응답 필드 추정 (result.rate 또는 result.exchangeRate)
  const r = data.result ?? data;
  return {
    rate: parseFloat(r.rate ?? r.usdKrw ?? r.exchangeRate ?? "1380") || 1380,
    updatedAt: r.updatedAt ?? r.timestamp ?? new Date().toISOString(),
  };
}

// Mock 모드 여부
export function isMockMode(): boolean {
  return !process.env.TOSS_CLIENT_ID || !process.env.TOSS_CLIENT_SECRET;
}

// Mock 데이터
export function generateMockPrices(symbols: string[]): StockPrice[] {
  const seed = (s: string) => s.split("").reduce((a, c) => a + c.charCodeAt(0), 0);
  return symbols.map((symbol) => {
    const isUS = /^[A-Z]{1,5}$/.test(symbol);
    const base = isUS ? 100 + (seed(symbol) % 900) : 50000 + (seed(symbol) % 200000);
    const changeRate = ((seed(symbol) % 1001) - 500) / 100;
    const change = Math.round(base * (changeRate / 100));
    return {
      symbol,
      price: base,
      change,
      changeRate,
      volume: 100000 + (seed(symbol) % 5000000),
      currency: isUS ? "USD" : "KRW",
    };
  });
}

export function generateMockCandles(symbol: string, count = 60): Candle[] {
  const seed = symbol.split("").reduce((a, c) => a + c.charCodeAt(0), 0);
  const isUS = /^[A-Z]{1,5}$/.test(symbol);
  let price = isUS ? 100 + (seed % 900) : 50000 + (seed % 200000);
  const candles: Candle[] = [];
  const now = new Date();
  for (let i = count; i >= 0; i--) {
    const d = new Date(now);
    d.setDate(d.getDate() - i);
    const change = (((seed * (i + 1)) % 11) - 5) / 100;
    const open = price;
    price = Math.round(price * (1 + change));
    candles.push({
      time: d.toISOString().split("T")[0],
      open,
      high: Math.round(Math.max(open, price) * 1.01),
      low: Math.round(Math.min(open, price) * 0.99),
      close: price,
      volume: 100000 + ((seed * i) % 1000000),
    });
  }
  return candles;
}
