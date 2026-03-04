/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'ha-background': 'var(--primary-background-color)',
        'ha-card': 'var(--card-background-color)',
        'ha-text': 'var(--primary-text-color)',
        'ha-secondary-text': 'var(--secondary-text-color)',
        'ha-border': 'var(--divider-color)',
        'ha-accent': 'var(--accent-color)',
        'ha-primary': 'var(--primary-color)',
        'ha-hover': 'var(--secondary-background-color)',
      },
      borderRadius: {
        'ha': 'var(--ha-card-border-radius, 12px)',
      },
    },
  },
  plugins: [],
};
