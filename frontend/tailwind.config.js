/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        industrial: {
          950: '#070B11',
          900: '#0B111B',
          850: '#101826',
          800: '#162234',
          700: '#23344D',
          muted: '#64748B',
          text: '#94A3B8',
          heading: '#F8FAFC'
        },
        alarm: {
          critical: '#EF4444',
          warning: '#F59E0B',
          nominal: '#10B981',
          info: '#3B82F6'
        }
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
        sans: ['Inter', 'system-ui', 'sans-serif']
      }
    },
  },
  plugins: [],
}