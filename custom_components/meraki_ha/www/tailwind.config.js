/** @type {import('tailwindcss').Config} */
export default {
<<<<<<< HEAD
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
=======
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'cisco-blue': '#00bceb',
        light: {
          background: '#f8f9fa',
          card: '#ffffff',
          text: '#212529',
          border: '#dee2e6',
        },
        dark: {
          background: '#121212',
          card: '#1e1e1e',
          text: '#e8eaed',
          border: '#3c4043',
        },
      },
    },
  },
  plugins: [],
};
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
