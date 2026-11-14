import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// En desarrollo, Vite reenvía /api al backend de Python (puerto 8000).
// En producción, FastAPI sirve directamente la carpeta dist/ (monolito).
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: { "/api": "http://localhost:8000" },
  },
});
