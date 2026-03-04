import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    // Empty the output directory before building
    emptyOutDir: true,
    rollupOptions: {
      output: {
        // Force the main entry file to match your postbuild script
        entryFileNames: 'meraki-panel.js',
        
        // Remove hashes from chunk and asset files as well
        chunkFileNames: '[name].js',
        assetFileNames: 'assets/[name].[ext]'
      }
    }
  }
});
