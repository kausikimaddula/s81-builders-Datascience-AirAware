/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        shell: "#fcfaf6",
        ink: "#111827",
        mist: "#d6e7df",
        coral: "#f97360",
        ocean: "#0f766e",
        slate: "#334155",
      },
      fontFamily: {
        display: ["Sora", "sans-serif"],
        body: ["Space Grotesk", "sans-serif"],
      },
      boxShadow: {
        soft: "0 18px 50px rgba(17, 24, 39, 0.12)",
      },
      animation: {
        rise: "rise 0.6s ease-out both",
      },
      keyframes: {
        rise: {
          "0%": { opacity: 0, transform: "translateY(16px)" },
          "100%": { opacity: 1, transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};
