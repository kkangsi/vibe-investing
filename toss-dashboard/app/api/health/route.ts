import { NextResponse } from "next/server";
import { isMockMode } from "@/lib/toss";

export async function GET() {
  return NextResponse.json({
    status: "ok",
    mode: isMockMode() ? "MOCK" : "LIVE",
    hasDb: !!process.env.DATABASE_URL,
    hasRedis: !!process.env.UPSTASH_REDIS_REST_URL,
    timestamp: new Date().toISOString(),
  });
}
