import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");

  return {
    plugins: [react()],
    base: env.VITE_BUILD_BASE || "/",
    server: {
      port: 5173,
      host: "0.0.0.0",
      allowedHosts: ["angel-respondents-era-republic.trycloudflare.com"],
      proxy: {
        "/api": {
          target: "http://127.0.0.1:8000",
          changeOrigin: true
        }
      }
    }
  };
});
