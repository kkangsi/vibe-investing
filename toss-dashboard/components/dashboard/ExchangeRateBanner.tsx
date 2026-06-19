"use client";
import { useEffect, useState } from "react";

export function ExchangeRateBanner() {
  const [rate, setRate] = useState<number | null>(null);
  const [updatedAt, setUpdatedAt] = useState<string>("");

  useEffect(() => {
    fetch("/api/toss/exchange-rate")
      .then((r) => r.json())
      .then((d) => {
        setRate(d.data?.rate ?? null);
        setUpdatedAt(d.data?.updatedAt ?? "");
      })
      .catch(() => {});

    const timer = setInterval(() => {
      fetch("/api/toss/exchange-rate")
        .then((r) => r.json())
        .then((d) => {
          setRate(d.data?.rate ?? null);
          setUpdatedAt(d.data?.updatedAt ?? "");
        })
        .catch(() => {});
    }, 60_000);

    return () => clearInterval(timer);
  }, []);

  if (!rate) return null;

  return (
    <div className="flex items-center gap-2 text-sm text-toss-gray-500">
      <span className="text-toss-gray-400">USD/KRW</span>
      <span className="font-semibold text-toss-gray-700 tabular-nums">
        {rate.toLocaleString("ko-KR")}원
      </span>
      {updatedAt && (
        <span className="text-xs text-toss-gray-400">
          {new Date(updatedAt).toLocaleTimeString("ko-KR", {
            hour: "2-digit",
            minute: "2-digit",
          })}
          기준
        </span>
      )}
    </div>
  );
}
