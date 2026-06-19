"use client";

interface MockBannerProps {
  isMock: boolean;
}

export function MockBanner({ isMock }: MockBannerProps) {
  if (!isMock) return null;

  return (
    <div className="bg-yellow-50 border border-yellow-200 rounded-xl px-4 py-3 flex items-center gap-2 text-sm">
      <span className="text-yellow-600">⚠️</span>
      <span className="text-yellow-800 font-medium">MOCK MODE</span>
      <span className="text-yellow-700">
        — .env.local에 TOSS_CLIENT_ID / TOSS_CLIENT_SECRET을 등록하면 실시간 데이터로 전환됩니다.
      </span>
    </div>
  );
}
