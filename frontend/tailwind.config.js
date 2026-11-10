/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#0B1120',
          900: '#101827',
          850: '#131D31',
          800: '#1E293B',
          700: '#334155',
        },
        gold: {
          300: '#F5E3C3',
          400: '#E5C07B',
          500: '#D6AD60',
          600: '#B8860B',
          700: '#8A6208',
        },
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'system-ui', 'sans-serif'],
        serif: ['Playfair Display', 'Georgia', 'serif'],
      },
      boxShadow: {
        'gold-glow': '0 0 25px -5px rgba(214, 173, 96, 0.3)',
        'gold-card': '0 20px 45px -10px rgba(214, 173, 96, 0.25)',
      },
    },
  },
  plugins: [],
};

