import { defineConfig } from 'vite';
<<<<<<< HEAD

// https://vitejs.dev/config/
export default defineConfig({
  define: {
    'process.env.NODE_ENV': JSON.stringify('production'),
  },
  build: {
    lib: {
      entry: 'src/meraki-panel.ts',
      name: 'MerakiPanel',
      fileName: (format) => `meraki-panel.js`,
      formats: ['es'],
    },
    outDir: '.',
    sourcemap: false,
    minify: true,
  },
=======
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
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
});
