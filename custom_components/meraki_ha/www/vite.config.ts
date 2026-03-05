import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  const buildTarget = process.env.BUILD_TARGET || 'panel';
  const isCard = buildTarget === 'card';

  return {
    plugins: [react()],
    build: {
      // We handle emptying in the build script
      emptyOutDir: false,
      rollupOptions: {
        input: isCard ? 'src/meraki-guest-access-card.ts' : 'src/main.tsx',
        output: {
          entryFileNames: isCard ? 'meraki-guest-access-card.js' : 'meraki-panel.js',
          // Ensure a single self-contained file for Home Assistant
          inlineDynamicImports: true,
        },
      },
      // Prevent separate CSS file for the card
      cssCodeSplit: false,
      assetsInlineLimit: 1000000,
    },
  };
});
