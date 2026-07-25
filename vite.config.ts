import { defineConfig } from "vite";
import { resolve } from "node:path";

export default defineConfig({
  root: ".",
  resolve: {
    alias: {
      "@": resolve(__dirname, "src"),
    },
  },
  server: {
    host: true,
    port: 5173,
    // WebXR requires a secure context (HTTPS or localhost).
    // When testing on a headset over LAN, use `npm run preview` behind a tunnel
    // or enable HTTPS locally.
  },
  preview: {
    host: true,
    port: 4173,
  },
  build: {
    outDir: "dist",
    sourcemap: true,
  },
});
