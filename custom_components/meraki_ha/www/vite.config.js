import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    // Output a single IIFE bundle for Home Assistant panel
    lib: {
      entry: resolve(__dirname, 'src/main.tsx'),
      name: 'MerakiPanel',
      fileName: () => 'meraki-panel.js',
      formats: ['iife'],
    },
    // Output to a build directory, then we'll copy to root
    outDir: 'build',
    // Empty the output directory on build
    emptyOutDir: true,
    rollupOptions: {
      output: {
        // Ensure all code is in one file
        inlineDynamicImports: true,
        // Don't add hash to filename
        entryFileNames: 'meraki-panel.js',
        assetFileNames: 'style.css',
      },
    },
    // Generate sourcemaps for debugging
    sourcemap: true,
    // Use esbuild minification (built-in, no extra dependency)
    minify: 'esbuild',
  },
  // Define global constants
  define: {
    'process.env.NODE_ENV': JSON.stringify('production'),
  },
});
