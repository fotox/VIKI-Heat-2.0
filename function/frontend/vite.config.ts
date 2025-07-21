import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  base: '/',
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://viki-backend:5000',
        changeOrigin: true,
      },
      '/socket.io': {
        target: 'http://viki-backend:5000',
        ws: true,
        changeOrigin: true,
      },
    },
  },
})
