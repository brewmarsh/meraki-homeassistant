import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  define: {
    'process.env.NODE_ENV': JSON.stringify('production'),
  },
  build: {
    lib: {
      entry: 'src/main.tsx',
      name: 'MerakiPanel',
      fileName: (format) => `meraki-panel.js`,
      formats: ['es'],
    },
    outDir: '.',
    sourcemap: false,
    minify: true,
  },
});
