import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    lib: {
      entry: 'src/main.tsx',
      name: 'MerakiPanel',
      fileName: (format) => `meraki-panel.js`,
      formats: ['es'],
    },
    rollupOptions: {
      // Don't bundle react, it's provided by Home Assistant
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
        },
      },
    },
    outDir: '.',
    sourcemap: false,
    minify: true,
  },
});
