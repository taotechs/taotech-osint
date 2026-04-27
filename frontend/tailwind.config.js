/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        cyber: {
          bg: "#090d1a",
          panel: "#0f172a",
          panelSoft: "#131c31",
          border: "#1f2a44",
          accent: "#00f5ff",
          success: "#22c55e",
          danger: "#ef4444",
        },
      },
      boxShadow: {
        glow: "0 0 20px rgba(0, 245, 255, 0.2)",
      },
    },
  },
  plugins: [],
};
