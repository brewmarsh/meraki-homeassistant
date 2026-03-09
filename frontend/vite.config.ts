import { defineConfig } from 'vite';
import { resolve } from 'path';
import { readFileSync } from 'fs';

// Read package.json to sync the version string
const pkg = JSON.parse(readFileSync(resolve(__dirname, 'package.json'), 'utf-8'));

export default defineConfig({
  define: {
    // Priority: beta branch. Uses semantic versioning from package.json
    __VERSION__: JSON.stringify(pkg.version),
  },
  build: {
    lib: {
      entry: resolve(__dirname, 'src/meraki-guest-access-card.ts'),
      name: 'MerakiCard',
      fileName: () => 'meraki-card.js',
      formats: ['es'],
    },
    // Output directly to the integration's www folder for Home Assistant access
    outDir: resolve(__dirname, '../custom_components/meraki_ha/www'),
    emptyOutDir: false,
    rollupOptions: {
      output: {
        entryFileNames: 'meraki-card.js',
      },
    },
  },
});