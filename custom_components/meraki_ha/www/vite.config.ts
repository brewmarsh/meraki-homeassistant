import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  build: {
    lib: {
      entry: path.resolve(__dirname, 'src/meraki-guest-access-card.ts'),
      name: 'MerakiCard',
      formats: ['es'],
      fileName: () => 'meraki-card.js',
    },
    outDir: '.',
    emptyOutDir: false,
    rollupOptions: {
      // Bundle all dependencies to create a standalone ES module
      external: [],
    },
  },
});
