import { describe, it, expect } from "vitest";
import { SYMBOLS, searchSymbols, SYM_BY_TICKER, WATCHLIST_TICKERS, ETF_TICKERS } from "../../shared/symbols";

describe("symbols 사전", () => {
  it("티커 중복 없음", () => {
    const tickers = SYMBOLS.map((s) => s.t);
    expect(new Set(tickers).size).toBe(tickers.length);
  });

  it("검색: 티커 / 영문명 / 한글명 / 약칭", () => {
    expect(searchSymbols("NVDA").map((s) => s.t)).toContain("NVDA");
    expect(searchSymbols("tesla").map((s) => s.t)).toContain("TSLA");
    expect(searchSymbols("엔비디아").map((s) => s.t)).toContain("NVDA");
    expect(searchSymbols("엔비").map((s) => s.t)).toContain("NVDA"); // 약칭
    expect(searchSymbols("구글").map((s) => s.t)).toEqual(expect.arrayContaining(["GOOGL", "GOOG"]));
  });

  it("한국 선호 ETF 한글/약칭 검색", () => {
    expect(searchSymbols("반도체").map((s) => s.t)).toEqual(expect.arrayContaining(["SOXL", "SOXX", "SMH"]));
    expect(searchSymbols("슈드").map((s) => s.t)).toContain("SCHD");
    expect(searchSymbols("나스닥").map((s) => s.t)).toContain("QQQ");
  });

  it("정확 티커가 접두/부분일치보다 우선", () => {
    expect(searchSymbols("AMD")[0].t).toBe("AMD");
  });

  it("빈 쿼리는 빈 결과", () => {
    expect(searchSymbols("")).toEqual([]);
    expect(searchSymbols("   ")).toEqual([]);
  });

  it("워치리스트=빅테크+AI, ETF 그룹 분리", () => {
    expect(WATCHLIST_TICKERS).toEqual(expect.arrayContaining(["AAPL", "NVDA", "VRT"]));
    expect(WATCHLIST_TICKERS).not.toContain("QQQ"); // ETF 는 워치리스트 아님
    expect(ETF_TICKERS).toEqual(expect.arrayContaining(["QQQ", "TQQQ", "SCHD"]));
  });

  it("SYM_BY_TICKER 조회", () => {
    expect(SYM_BY_TICKER["NVDA"].ko).toBe("엔비디아");
  });
});
