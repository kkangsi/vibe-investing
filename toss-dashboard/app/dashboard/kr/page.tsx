import { getPrices, generateMockPrices, isMockMode } from "@/lib/toss";
import { KR_SECTORS, findStock } from "@/lib/universe";
import { PriceTable } from "@/components/dashboard/PriceTable";
import { MockBanner } from "@/components/dashboard/MockBanner";
import type { DashboardStock } from "@/types/toss";

async function getData() {
  const allSymbols = KR_SECTORS.flatMap((sec) => sec.stocks.map((s) => s.symbol));

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

  const sectorData = KR_SECTORS.map((sector) => {
    const stocks: DashboardStock[] = sector.stocks.map((s) => {
      const p = prices.find((x) => x.symbol === s.symbol);
      const info = findStock(s.symbol);
      return {
        symbol: s.symbol,
        name: info?.name ?? s.name,
        price: p?.price ?? 0,
        change: p?.change ?? 0,
        changeRate: p?.changeRate ?? 0,
        volume: p?.volume ?? 0,
        currency: "KRW" as const,
        market: "KR" as const,
        sector: s.sector,
        tag: info?.tag,
      };
    });

    const avgChange =
      stocks.reduce((sum, s) => sum + s.changeRate, 0) / stocks.length;

    return { ...sector, stocks, avgChange };
  });

  // 마켓 지표 (KOSPI proxy: KODEX 200 069500)
  const kodex200 = prices.find((p) => p.symbol === "069500");

  return { sectorData, mock, kodex200 };
}

export const revalidate = 30;

export default async function KrPage() {
  const { sectorData, mock, kodex200 } = await getData();

  const now = new Date();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-toss-gray-900">
          🇰🇷 한국 주식 & 지표
        </h1>
        <p className="text-toss-gray-500 mt-1 text-sm">
          KOSPI 섹터별 실시간 현황
        </p>
      </div>

      <MockBanner isMock={mock} />

      {/* 시장 지표 요약 */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <MarketCard
          label="KOSPI (KODEX 200)"
          value={kodex200?.price ? `${kodex200.price.toLocaleString()}원` : "-"}
          changeRate={kodex200?.changeRate}
        />
        <MarketCard
          label="업종 평균 등락"
          value={`${(sectorData.reduce((s, d) => s + d.avgChange, 0) / sectorData.length).toFixed(2)}%`}
          neutral
        />
        <MarketCard
          label="상승 섹터"
          value={`${sectorData.filter((s) => s.avgChange > 0).length}개`}
          positive
        />
        <MarketCard
          label="하락 섹터"
          value={`${sectorData.filter((s) => s.avgChange < 0).length}개`}
          negative
        />
      </div>

      {/* 섹터별 히트맵 */}
      <div>
        <h2 className="text-lg font-bold text-toss-gray-900 mb-3">섹터 히트맵</h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {sectorData.map((sector) => {
            const rate = sector.avgChange;
            const isUp = rate >= 0;
            return (
              <div
                key={sector.name}
                className={`rounded-xl p-3 ${isUp ? "bg-red-50 border border-red-100" : "bg-blue-50 border border-blue-100"}`}
              >
                <div className="text-xs font-medium text-toss-gray-700">
                  {sector.name}
                </div>
                <div
                  className={`text-lg font-bold tabular-nums ${isUp ? "text-toss-red" : "text-toss-blue"}`}
                >
                  {isUp ? "+" : ""}
                  {rate.toFixed(2)}%
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 섹터별 종목 테이블 */}
      {sectorData.map((sector) => (
        <PriceTable
          key={sector.name}
          stocks={sector.stocks}
          title={sector.name}
          showRank={false}
        />
      ))}

      <p className="text-xs text-toss-gray-400 text-right">
        {now.toLocaleString("ko-KR")} 기준 · 종목 클릭 시 차트
      </p>
    </div>
  );
}

function MarketCard({
  label,
  value,
  changeRate,
  positive,
  negative,
  neutral,
}: {
  label: string;
  value: string;
  changeRate?: number;
  positive?: boolean;
  negative?: boolean;
  neutral?: boolean;
}) {
  const isUp = changeRate !== undefined ? changeRate >= 0 : positive;
  const isDown = changeRate !== undefined ? changeRate < 0 : negative;

  return (
    <div className="bg-white rounded-2xl p-4 border border-toss-gray-100">
      <div className="text-xs text-toss-gray-500 mb-1">{label}</div>
      <div
        className={`text-lg font-bold tabular-nums ${
          isUp ? "text-toss-red" : isDown ? "text-toss-blue" : "text-toss-gray-900"
        }`}
      >
        {value}
      </div>
      {changeRate !== undefined && (
        <div
          className={`text-xs font-semibold ${
            changeRate >= 0 ? "text-toss-red" : "text-toss-blue"
          }`}
        >
          {changeRate >= 0 ? "+" : ""}
          {changeRate.toFixed(2)}%
        </div>
      )}
    </div>
  );
}
