import { getPrices, generateMockPrices, isMockMode } from "@/lib/toss";
import { POPULAR_KR_STOCKS, POPULAR_KR_ETFS, findStock } from "@/lib/universe";
import { PriceTable } from "@/components/dashboard/PriceTable";
import { MockBanner } from "@/components/dashboard/MockBanner";
import type { DashboardStock } from "@/types/toss";

async function getData() {
  const krSymbols = POPULAR_KR_STOCKS.map((s) => s.symbol);
  const etfSymbols = POPULAR_KR_ETFS.map((s) => s.symbol);
  const allSymbols = [...krSymbols, ...etfSymbols];

  let prices;
  let mock = false;

  if (isMockMode()) {
    prices = generateMockPrices(allSymbols);
    mock = true;
  } else {
    try {
      prices = await getPrices(allSymbols);
    } catch {
      prices = generateMockPrices(allSymbols);
      mock = true;
    }
  }

  const toStock = (symbol: string): DashboardStock => {
    const p = prices.find((x) => x.symbol === symbol);
    const info = findStock(symbol);
    return {
      symbol,
      name: info?.name ?? symbol,
      nameKr: info?.nameKr,
      price: p?.price ?? 0,
      change: p?.change ?? 0,
      changeRate: p?.changeRate ?? 0,
      volume: p?.volume ?? 0,
      currency: p?.currency ?? "KRW",
      market: info?.market ?? "KR",
      sector: info?.sector,
      tag: info?.tag,
    };
  };

  return {
    krStocks: krSymbols.map(toStock),
    etfs: etfSymbols.map(toStock),
    mock,
  };
}

export const revalidate = 30;

export default async function PopularPage() {
  const { krStocks, etfs, mock } = await getData();

  // 등락률 내림차순 TOP 상승/하락
  const sorted = [...krStocks].sort((a, b) => b.changeRate - a.changeRate);
  const topGainers = sorted.slice(0, 5);
  const topLosers = [...sorted].reverse().slice(0, 5);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-toss-gray-900">
          🔥 한국인들이 사랑하는 주식 & ETF
        </h1>
        <p className="text-toss-gray-500 mt-1 text-sm">
          국내 개인투자자들이 가장 많이 거래하는 종목 실시간 현황
        </p>
      </div>

      <MockBanner isMock={mock} />

      {/* 상승/하락 요약 */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-toss-red-light rounded-2xl p-4">
          <div className="text-sm font-semibold text-toss-red mb-3">
            📈 오늘의 상위 상승
          </div>
          <div className="space-y-2">
            {topGainers.map((s, i) => (
              <div key={s.symbol} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-xs text-toss-gray-400 w-4">{i + 1}</span>
                  <span className="text-sm font-medium text-toss-gray-900">
                    {s.name}
                  </span>
                </div>
                <span className="text-sm font-bold text-toss-red tabular-nums">
                  +{s.changeRate.toFixed(2)}%
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-blue-50 rounded-2xl p-4">
          <div className="text-sm font-semibold text-toss-blue mb-3">
            📉 오늘의 상위 하락
          </div>
          <div className="space-y-2">
            {topLosers.map((s, i) => (
              <div key={s.symbol} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-xs text-toss-gray-400 w-4">{i + 1}</span>
                  <span className="text-sm font-medium text-toss-gray-900">
                    {s.name}
                  </span>
                </div>
                <span className="text-sm font-bold text-toss-blue tabular-nums">
                  {s.changeRate.toFixed(2)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 인기 주식 전체 */}
      <PriceTable
        stocks={krStocks}
        title="🏆 인기 주식 TOP"
        showRank
      />

      {/* ETF */}
      <PriceTable
        stocks={etfs}
        title="📊 인기 ETF"
        showRank
      />

      <p className="text-xs text-toss-gray-400 text-right">
        종목 클릭 시 차트 · 30초마다 자동 갱신
      </p>
    </div>
  );
}
