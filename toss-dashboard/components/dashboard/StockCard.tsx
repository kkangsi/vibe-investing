"use client";
import { useState } from "react";
import { cn, formatPrice, formatChangeRate, formatVolume } from "@/lib/utils";
import type { DashboardStock } from "@/types/toss";
import { MiniChart } from "./MiniChart";

interface StockCardProps {
  stock: DashboardStock;
  rank?: number;
}

export function StockCard({ stock, rank }: StockCardProps) {
  const [showChart, setShowChart] = useState(false);
  const isUp = stock.changeRate >= 0;
  const isDown = stock.changeRate < 0;

  return (
    <div
      className={cn(
        "bg-white rounded-2xl p-4 border border-toss-gray-100 hover:border-toss-blue/30 hover:shadow-sm transition-all cursor-pointer select-none",
        showChart && "border-toss-blue/30 shadow-sm"
      )}
      onClick={() => setShowChart((v) => !v)}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-3 min-w-0">
          {rank && (
            <span className="text-sm font-bold text-toss-gray-400 w-5 shrink-0">
              {rank}
            </span>
          )}
          <div className="min-w-0">
            <div className="flex items-center gap-1.5 flex-wrap">
              <span className="font-semibold text-toss-gray-900 truncate">
                {stock.name}
              </span>
              {stock.tag && (
                <span className="text-xs bg-toss-gray-100 text-toss-gray-600 px-1.5 py-0.5 rounded-full whitespace-nowrap">
                  {stock.tag}
                </span>
              )}
            </div>
            <div className="flex items-center gap-1.5 mt-0.5">
              <span className="text-xs text-toss-gray-400">{stock.symbol}</span>
              {stock.sector && (
                <span className="text-xs text-toss-gray-400">· {stock.sector}</span>
              )}
            </div>
          </div>
        </div>

        <div className="text-right shrink-0">
          <div className="font-bold text-toss-gray-900 tabular-nums">
            {formatPrice(stock.price, stock.currency)}
          </div>
          <div
            className={cn(
              "text-sm font-semibold tabular-nums",
              isUp && "text-toss-red",
              isDown && "text-toss-blue",
              !isUp && !isDown && "text-toss-gray-500"
            )}
          >
            {formatChangeRate(stock.changeRate)}
          </div>
          <div className="text-xs text-toss-gray-400 mt-0.5">
            {formatVolume(stock.volume)}
          </div>
        </div>
      </div>

      {showChart && (
        <div className="mt-3 pt-3 border-t border-toss-gray-100">
          <MiniChart symbol={stock.symbol} />
        </div>
      )}
    </div>
  );
}
