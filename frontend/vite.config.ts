import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    lib: {
      entry: resolve(__dirname, 'src/meraki-guest-access-card.ts'),
      name: 'MerakiCard',
      fileName: () => 'meraki-card.js',
      formats: ['es'],
    },
    outDir: resolve(__dirname, '../custom_components/meraki_ha/www'),
    emptyOutDir: false,
    rollupOptions: {
      output: {
        entryFileNames: 'meraki-card.js',
      },
    },
  },
});
