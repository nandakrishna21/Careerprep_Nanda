import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Fast refresh: skip pre-bundling churn, keep HMR overlay quiet.
    hmr: { overlay: false },
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  optimizeDeps: {
    include: ['react', 'react-dom', 'react-router-dom', 'axios', 'zustand'],
    // recharts is huge — exclude from pre-bundle so dev refresh stays fast,
    // it loads lazily only on Dashboard.
    exclude: ['recharts'],
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    // Faster cold builds + smaller refresh payloads.
    target: 'esnext',
    cssCodeSplit: true,
    chunkSizeWarningLimit: 600,
    rollupOptions: {
      output: {
        // Keep framework, charts, and utils in separate chunks so a refresh
        // on /gov/pyqs never re-downloads the 380kB chart lib.
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          charts: ['recharts'],
          utils: ['axios', 'zustand'],
        },
      },
    },
  },
});
