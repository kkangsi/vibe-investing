"use client";
import { cn, formatPrice, formatChangeRate, formatVolume } from "@/lib/utils";
import type { DashboardStock } from "@/types/toss";
import { MiniChart } from "./MiniChart";
import { useState } from "react";

interface PriceTableProps {
  stocks: DashboardStock[];
  title?: string;
  showRank?: boolean;
}

export function PriceTable({ stocks, title, showRank }: PriceTableProps) {
  const [expanded, setExpanded] = useState<string | null>(null);

  return (
    <div>
      {title && (
        <h2 className="text-lg font-bold text-toss-gray-900 mb-3">{title}</h2>
      )}
      <div className="bg-white rounded-2xl border border-toss-gray-100 overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-toss-gray-100">
              {showRank && (
                <th className="text-left py-3 px-4 text-xs font-medium text-toss-gray-500 w-8">
                  #
                </th>
              )}
              <th className="text-left py-3 px-4 text-xs font-medium text-toss-gray-500">
                종목
              </th>
              <th className="text-right py-3 px-4 text-xs font-medium text-toss-gray-500">
                현재가
              </th>
              <th className="text-right py-3 px-4 text-xs font-medium text-toss-gray-500">
                등락률
              </th>
              <th className="text-right py-3 px-4 text-xs font-medium text-toss-gray-500 hidden md:table-cell">
                거래량
              </th>
            </tr>
          </thead>
          <tbody>
            {stocks.map((stock, idx) => {
              const isUp = stock.changeRate >= 0;
              const isExpanded = expanded === stock.symbol;
              return (
                <>
                  <tr
                    key={stock.symbol}
                    className={cn(
                      "border-b border-toss-gray-100 last:border-0 hover:bg-toss-gray-50 cursor-pointer transition-colors",
                      isExpanded && "bg-toss-gray-50"
                    )}
                    onClick={() =>
                      setExpanded(isExpanded ? null : stock.symbol)
                    }
                  >
                    {showRank && (
                      <td className="py-3 px-4 text-sm font-bold text-toss-gray-400">
                        {idx + 1}
                      </td>
                    )}
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2">
                        <div>
                          <div className="font-semibold text-toss-gray-900 text-sm">
                            {stock.name}
                          </div>
                          <div className="text-xs text-toss-gray-400 flex items-center gap-1">
                            <span>{stock.symbol}</span>
                            {stock.tag && (
                              <span className="bg-toss-gray-100 text-toss-gray-600 px-1 py-0.5 rounded-full">
                                {stock.tag}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-4 text-right font-bold tabular-nums text-sm text-toss-gray-900">
                      {formatPrice(stock.price, stock.currency)}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <span
                        className={cn(
                          "font-semibold tabular-nums text-sm",
                          isUp ? "text-toss-red" : "text-toss-blue"
                        )}
                      >
                        {formatChangeRate(stock.changeRate)}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right text-xs text-toss-gray-400 hidden md:table-cell">
                      {formatVolume(stock.volume)}
                    </td>
                  </tr>
                  {isExpanded && (
                    <tr key={`chart-${stock.symbol}`} className="bg-toss-gray-50">
                      <td colSpan={showRank ? 5 : 4} className="px-4 pb-4">
                        <MiniChart symbol={stock.symbol} />
                      </td>
                    </tr>
                  )}
                </>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
