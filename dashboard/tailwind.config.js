/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#09090b', // Zinc 950
        card: '#18181b', // Zinc 900
        border: '#27272a', // Zinc 800
        primary: {
          DEFAULT: '#3b82f6', // Blue 500
          dark: '#1d4ed8', // Blue 700
          light: '#60a5fa', // Blue 400
        },
        risk: {
          low: '#22c55e', // Green 500
          medium: '#eab308', // Yellow 500
          high: '#ef4444', // Red 500
        }
      },
      fontFamily: {
        sans: ['Outfit', 'Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
