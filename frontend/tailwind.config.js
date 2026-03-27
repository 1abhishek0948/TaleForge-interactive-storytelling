/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0f172a",
        dusk: "#1e293b",
        ember: "#d97706",
        mint: "#10b981",
        cloud: "#e2e8f0"
      },
      boxShadow: {
        soft: "0 20px 45px -20px rgba(15, 23, 42, 0.35)"
      }
    }
  },
  plugins: []
};
