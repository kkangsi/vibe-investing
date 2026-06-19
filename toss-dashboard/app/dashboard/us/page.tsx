import { getPrices, generateMockPrices, isMockMode, getExchangeRate } from "@/lib/toss";
import { US_STOCKS, US_ETFS, findStock } from "@/lib/universe";
import { PriceTable } from "@/components/dashboard/PriceTable";
import { MockBanner } from "@/components/dashboard/MockBanner";
import type { DashboardStock } from "@/types/toss";

async function getData() {
  const stockSymbols = US_STOCKS.map((s) => s.symbol);
  const etfSymbols = US_ETFS.map((s) => s.symbol);
  const allSymbols = [...stockSymbols, ...etfSymbols];

  let prices;
  let mock = false;
  let exchangeRate = 1380;

  if (isMockMode()) {
    prices = generateMockPrices(allSymbols);
    mock = true;
  } else {
    try {
      [prices] = await Promise.all([getPrices(allSymbols)]);
      try {
        const fx = await getExchangeRate();
        exchangeRate = fx.rate;
      } catch {}
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
      name: info?.nameKr ?? info?.name ?? symbol,
      nameKr: info?.nameKr,
      price: p?.price ?? 0,
      change: p?.change ?? 0,
      changeRate: p?.changeRate ?? 0,
      volume: p?.volume ?? 0,
      currency: "USD",
      market: "US",
      sector: info?.sector,
      tag: info?.tag,
    };
  };

  const stocks = stockSymbols.map(toStock);
  const etfs = etfSymbols.map(toStock);

  // 섹터별 그룹핑
  const sectorMap = new Map<string, DashboardStock[]>();
  stocks.forEach((s) => {
    const sec = s.sector ?? "기타";
    if (!sectorMap.has(sec)) sectorMap.set(sec, []);
    sectorMap.get(sec)!.push(s);
  });

  return { stocks, etfs, sectorMap, mock, exchangeRate };
}

export const revalidate = 30;

export default async function UsPage() {
  const { stocks, etfs, sectorMap, mock, exchangeRate } = await getData();

  const spyPrice = etfs.find((e) => e.symbol === "SPY");
  const qqqPrice = etfs.find((e) => e.symbol === "QQQ");
  const nvdaPrice = stocks.find((s) => s.symbol === "NVDA");

  const sortedStocks = [...stocks].sort((a, b) => b.changeRate - a.changeRate);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-toss-gray-900">
          🇺🇸 미국 주식 & 지표
        </h1>
        <p className="text-toss-gray-500 mt-1 text-sm">
          한국 투자자들이 주목하는 미국 종목 실시간 현황
        </p>
      </div>

      <MockBanner isMock={mock} />

      {/* 주요 지표 */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <UsCard
          label="S&P 500 (SPY)"
          value={spyPrice ? `$${spyPrice.price.toFixed(2)}` : "-"}
          changeRate={spyPrice?.changeRate}
        />
        <UsCard
          label="나스닥 100 (QQQ)"
          value={qqqPrice ? `$${qqqPrice.price.toFixed(2)}` : "-"}
          changeRate={qqqPrice?.changeRate}
        />
        <UsCard
          label="NVIDIA"
          value={nvdaPrice ? `$${nvdaPrice.price.toFixed(2)}` : "-"}
          changeRate={nvdaPrice?.changeRate}
        />
        <div className="bg-white rounded-2xl p-4 border border-toss-gray-100">
          <div className="text-xs text-toss-gray-500 mb-1">원/달러 환율</div>
          <div className="text-lg font-bold text-toss-gray-900 tabular-nums">
            {exchangeRate.toLocaleString("ko-KR")}원
          </div>
          <div className="text-xs text-toss-gray-400 mt-0.5">1 USD</div>
        </div>
      </div>

      {/* 오늘의 상위 등락 */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-toss-red-light rounded-2xl p-4">
          <div className="text-sm font-semibold text-toss-red mb-3">
            🚀 오늘의 상승
          </div>
          <div className="space-y-2">
            {sortedStocks.slice(0, 5).map((s, i) => (
              <div key={s.symbol} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-xs text-toss-gray-400 w-4">{i + 1}</span>
                  <span className="text-sm font-medium text-toss-gray-900">
                    {s.name}
                  </span>
                </div>
                <span className="text-sm font-bold text-toss-red tabular-nums">
                  {s.changeRate >= 0 ? "+" : ""}{s.changeRate.toFixed(2)}%
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-blue-50 rounded-2xl p-4">
          <div className="text-sm font-semibold text-toss-blue mb-3">
            📉 오늘의 하락
          </div>
          <div className="space-y-2">
            {[...sortedStocks].reverse().slice(0, 5).map((s, i) => (
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

      {/* 섹터별 */}
      {Array.from(sectorMap.entries()).map(([sector, sectorStocks]) => (
        <PriceTable
          key={sector}
          stocks={sectorStocks}
          title={`${sector}`}
          showRank={false}
        />
      ))}

      {/* ETF */}
      <PriceTable stocks={etfs} title="📊 미국 ETF" showRank={false} />

      <p className="text-xs text-toss-gray-400 text-right">
        종목 클릭 시 차트 · 미국 장 운영시간 22:30~05:00 (한국시간)
      </p>
    </div>
  );
}

function UsCard({
  label,
  value,
  changeRate,
}: {
  label: string;
  value: string;
  changeRate?: number;
}) {
  const isUp = (changeRate ?? 0) >= 0;

  return (
    <div className="bg-white rounded-2xl p-4 border border-toss-gray-100">
      <div className="text-xs text-toss-gray-500 mb-1">{label}</div>
      <div className="text-lg font-bold text-toss-gray-900 tabular-nums">
        {value}
      </div>
      {changeRate !== undefined && (
        <div
          className={`text-xs font-semibold tabular-nums ${
            isUp ? "text-toss-red" : "text-toss-blue"
          }`}
        >
          {isUp ? "+" : ""}
          {changeRate.toFixed(2)}%
        </div>
      )}
    </div>
  );
}
