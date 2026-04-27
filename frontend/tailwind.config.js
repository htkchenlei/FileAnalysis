/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#B8A9C9', // 薰衣草紫
        secondary: '#A8E6CF', // 薄荷绿
        accent: '#FFB7B2', // 珊瑚粉
        background: '#FFF9F0', // 奶油白
        'card-bg': '#FFF5F5', // 浅粉白
        'text-primary': '#4A4A4A', // 深灰
        'text-secondary': '#8A8A8A', // 中灰
        border: '#E8E8E8', // 浅灰
        success: '#7DD3A8', // 柔绿
        warning: '#FFD199', // 柔橙
        error: '#FF9B9B', // 柔红
      },
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
      },
      boxShadow: {
        card: '0 4px 12px rgba(0, 0, 0, 0.08)',
        hover: '0 8px 24px rgba(0, 0, 0, 0.12)',
      },
      borderRadius: {
        card: '12px',
        button: '8px',
        container: '16px',
      },
      transitionDuration: {
        '200': '200ms',
      },
      transitionTimingFunction: {
        'ease-out': 'ease-out',
      },
    },
  },
  plugins: [],
}
