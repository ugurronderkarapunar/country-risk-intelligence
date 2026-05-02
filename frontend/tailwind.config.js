/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["DM Sans", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      colors: {
        surface: {
          900: "#0b0f14",
          800: "#111822",
          700: "#1a2332",
          600: "#243047",
        },
        accent: {
          cyan: "#22d3ee",
          violet: "#a78bfa",
          amber: "#fbbf24",
        },
      },
      boxShadow: {
        glow: "0 0 40px -10px rgba(34, 211, 238, 0.35)",
      },
    },
  },
  plugins: [],
};
