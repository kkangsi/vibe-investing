export interface TossToken {
  access_token: string;
  token_type: string;
  expires_in: number;
  issued_at: number;
}

export interface StockPrice {
  symbol: string;
  price: number;
  change: number;
  changeRate: number;
  volume: number;
  marketCap?: number;
  currency: "KRW" | "USD";
}

export interface Candle {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface StockInfo {
  symbol: string;
  name: string;
  market: "KR" | "US";
  currency: "KRW" | "USD";
  status: string;
  sector?: string;
}

export interface ExchangeRate {
  rate: number;
  updatedAt: string;
}

export interface MarketStatus {
  isOpen: boolean;
  session: string;
  nextOpen?: string;
}

export interface DashboardStock {
  symbol: string;
  name: string;
  nameKr?: string;
  price: number;
  change: number;
  changeRate: number;
  volume: number;
  currency: "KRW" | "USD";
  market: "KR" | "US";
  sector?: string;
  tag?: string;
  candles?: Candle[];
}

export type TabType = "popular" | "kr" | "us";
