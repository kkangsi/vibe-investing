"use client";
import { useEffect, useState } from "react";
import { AreaChart, Area, ResponsiveContainer, Tooltip, XAxis } from "recharts";
import type { Candle } from "@/types/toss";

interface MiniChartProps {
  symbol: string;
}

export function MiniChart({ symbol }: MiniChartProps) {
  const [candles, setCandles] = useState<Candle[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/toss/candles?symbol=${encodeURIComponent(symbol)}&count=30`)
      .then((r) => r.json())
      .then((d) => {
        setCandles(d.data ?? []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [symbol]);

  if (loading) {
    return (
      <div className="h-24 flex items-center justify-center text-xs text-toss-gray-400 animate-pulse">
        차트 로딩 중...
      </div>
    );
  }

  if (candles.length === 0) return null;

  const first = candles[0]?.close ?? 0;
  const last = candles[candles.length - 1]?.close ?? 0;
  const isUp = last >= first;
  const color = isUp ? "#F04452" : "#3182F6";

  return (
    <div className="h-24">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={candles} margin={{ top: 2, right: 0, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id={`grad-${symbol}`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={color} stopOpacity={0.2} />
              <stop offset="95%" stopColor={color} stopOpacity={0} />
            </linearGradient>
          </defs>
          <XAxis dataKey="time" hide />
          <Tooltip
            contentStyle={{
              background: "#191F28",
              border: "none",
              borderRadius: 8,
              fontSize: 11,
              color: "#fff",
            }}
            labelStyle={{ color: "#8B95A1" }}
            formatter={(v: number) => [v.toLocaleString(), "종가"]}
          />
          <Area
            type="monotone"
            dataKey="close"
            stroke={color}
            strokeWidth={2}
            fill={`url(#grad-${symbol})`}
            dot={false}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
