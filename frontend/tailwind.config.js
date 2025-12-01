/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'eco-bg': '#022c22',
        'eco-card': '#064e3b',
        'eco-accent': '#34d399',
        'eco-text': '#ecfdf5',
        'eco-dim': '#6ee7b7',
      }
    },
  },
  plugins: [],
}