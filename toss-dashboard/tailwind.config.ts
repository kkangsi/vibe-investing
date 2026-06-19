import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        toss: {
          blue: "#3182F6",
          "blue-dark": "#1B64DA",
          red: "#F04452",
          "red-light": "#FFF0F0",
          green: "#05C072",
          "green-light": "#E8FAF2",
          gray: {
            50: "#F9FAFB",
            100: "#F2F4F6",
            200: "#E5E8EB",
            300: "#D1D6DB",
            400: "#B0B8C1",
            500: "#8B95A1",
            600: "#6B7684",
            700: "#4E5968",
            800: "#333D4B",
            900: "#191F28",
          },
        },
      },
      fontFamily: {
        sans: [
          "-apple-system",
          "BlinkMacSystemFont",
          "Pretendard",
          "system-ui",
          "sans-serif",
        ],
      },
    },
  },
  plugins: [],
};

export default config;
