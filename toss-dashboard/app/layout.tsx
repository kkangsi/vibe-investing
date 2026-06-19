import type { Metadata } from "next";
import "./globals.css";
import Link from "next/link";
import { ExchangeRateBanner } from "@/components/dashboard/ExchangeRateBanner";
import { RefreshButton } from "@/components/dashboard/RefreshButton";
import { NavTabs } from "@/components/layout/NavTabs";

export const metadata: Metadata = {
  title: "TOSS x Vibe Invest",
  description: "토스증권 Open API 기반 실시간 주식 대시보드",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body className="min-h-screen bg-toss-gray-50">
        {/* Header */}
        <header className="sticky top-0 z-40 bg-white border-b border-toss-gray-100 shadow-sm">
          <div className="max-w-5xl mx-auto px-4">
            <div className="flex items-center justify-between h-14">
              <Link href="/dashboard/popular" className="flex items-center gap-2">
                <div className="w-7 h-7 rounded-lg bg-toss-blue flex items-center justify-center">
                  <span className="text-white text-xs font-bold">T</span>
                </div>
                <span className="font-bold text-toss-gray-900 hidden sm:block">
                  TOSS x Vibe Invest
                </span>
              </Link>

              <NavTabs />

              <div className="flex items-center gap-3">
                <ExchangeRateBanner />
                <RefreshButton />
              </div>
            </div>
          </div>
        </header>

        {/* Main */}
        <main className="max-w-5xl mx-auto px-4 py-6">{children}</main>

        {/* Footer */}
        <footer className="border-t border-toss-gray-100 mt-16 py-6">
          <div className="max-w-5xl mx-auto px-4 text-center text-xs text-toss-gray-400">
            토스증권 Open API 기반 · 투자 판단의 책임은 본인에게 있습니다 ·{" "}
            <a
              href="https://developers.tossinvest.com/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-toss-blue transition-colors"
            >
              Toss API Docs
            </a>
          </div>
        </footer>
      </body>
    </html>
  );
}
