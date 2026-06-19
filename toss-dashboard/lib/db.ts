import { neon } from "@neondatabase/serverless";

let sql: ReturnType<typeof neon> | null = null;

export function getDb() {
  if (!process.env.DATABASE_URL) return null;
  if (!sql) {
    sql = neon(process.env.DATABASE_URL);
  }
  return sql;
}

// 가격 스냅샷 저장 (선택적)
export async function savePriceSnapshot(
  symbol: string,
  price: number,
  changeRate: number
) {
  const db = getDb();
  if (!db) return;
  try {
    await db`
      INSERT INTO price_snapshots (symbol, price, change_rate, recorded_at)
      VALUES (${symbol}, ${price}, ${changeRate}, NOW())
      ON CONFLICT DO NOTHING
    `;
  } catch {
    // DB 없으면 무시
  }
}

// 스키마 초기화 (최초 1회 실행)
export async function initSchema() {
  const db = getDb();
  if (!db) return;
  await db`
    CREATE TABLE IF NOT EXISTS price_snapshots (
      id SERIAL PRIMARY KEY,
      symbol VARCHAR(20) NOT NULL,
      price NUMERIC NOT NULL,
      change_rate NUMERIC NOT NULL,
      recorded_at TIMESTAMPTZ DEFAULT NOW()
    )
  `;
}
