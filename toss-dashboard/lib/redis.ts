import { Redis } from "@upstash/redis";

let redis: Redis | null = null;

function getRedis(): Redis | null {
  const url = process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.UPSTASH_REDIS_REST_TOKEN;
  if (!url || !token) return null;
  // Upstash REST URL은 반드시 https:// 로 시작해야 함
  if (!url.startsWith("https://")) return null;
  if (!redis) {
    redis = new Redis({ url, token });
  }
  return redis;
}

export async function cacheGet<T>(key: string): Promise<T | null> {
  const client = getRedis();
  if (!client) return null;
  try {
    return await client.get<T>(key);
  } catch {
    return null;
  }
}

export async function cacheSet(key: string, value: unknown, ttlSeconds = 30): Promise<void> {
  const client = getRedis();
  if (!client) return;
  try {
    await client.set(key, value, { ex: ttlSeconds });
  } catch {
    // Redis 장애 시 무시
  }
}

export const CACHE_KEYS = {
  prices: (tab: string) => `toss:prices:${tab}`,
  exchangeRate: () => `toss:exchange-rate`,
  candles: (symbol: string) => `toss:candles:${symbol}`,
};
