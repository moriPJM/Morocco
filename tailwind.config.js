/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        morocco: {
          red: '#C1272D',
          green: '#006233',
          gold: '#FFD700',
          sand: '#F4A460',
          blue: '#4682B4'
        }
      },
      fontFamily: {
        'arabic': ['Noto Sans Arabic', 'Arial', 'sans-serif'],
        'berber': ['Noto Sans Tifinagh', 'Arial', 'sans-serif']
      }
    },
  },
  plugins: [],
}