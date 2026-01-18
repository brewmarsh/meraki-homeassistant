import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    lib: {
      entry: path.resolve(__dirname, 'src/entry.tsx'),
      name: 'MerakiPanel',
      fileName: () => 'meraki-panel.js',
      formats: ['es'],
    },
    outDir: '.',
    emptyOutDir: false,
  },
  define: {
    'process.env.NODE_ENV': '"production"',
  }
});
