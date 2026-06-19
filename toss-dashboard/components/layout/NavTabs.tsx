"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const NAV_TABS = [
  { href: "/dashboard/popular", label: "🔥 한국인의 선택", short: "인기" },
  { href: "/dashboard/kr", label: "🇰🇷 한국 주식", short: "한국" },
  { href: "/dashboard/us", label: "🇺🇸 미국 주식", short: "미국" },
];

export function NavTabs() {
  const pathname = usePathname();

  return (
    <nav className="flex items-center gap-1">
      {NAV_TABS.map((tab) => {
        const active = pathname === tab.href;
        return (
          <Link
            key={tab.href}
            href={tab.href}
            className={cn(
              "px-3 py-1.5 rounded-lg text-sm font-medium transition-colors",
              active
                ? "bg-toss-blue text-white"
                : "text-toss-gray-600 hover:text-toss-blue hover:bg-toss-blue/5"
            )}
          >
            <span className="hidden sm:inline">{tab.label}</span>
            <span className="sm:hidden">{tab.short}</span>
          </Link>
        );
      })}
    </nav>
  );
}
