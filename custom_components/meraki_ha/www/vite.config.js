import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  esbuild: {
    drop: ['debugger'], // Keep console.log, only drop debugger
    keepNames: true, // Keep original names for better debugging
  },
  build: {
    // Build directly to the current directory (www)
    outDir: '.',
    // Prevent Vite from emptying the directory and deleting source files
    emptyOutDir: false,
    rollupOptions: {
      output: {
        // Force the output filename to be meraki-panel.js
        entryFileNames: 'meraki-panel.js',
        // Ensure assets don't clutter the root
        assetFileNames: 'assets/[name]-[hash].[ext]',
        chunkFileNames: 'assets/[name]-[hash].js',
      },
    },
  },
});
