import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'
import svgLoader from 'vite-svg-loader'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    tailwindcss(),
    svgLoader(),
  ],
  // import.metaはECMAScript（ES）モジュールの仕様に含まれる、標準的なJavaScriptの構文
  // 現在実行されているモジュールに関するメタデータ（付加的な情報）を格納するためのオブジェクト
  // import.meta.urlで、設定ファイル（vite.config.js）自体の絶対URLを取得
  // new URL('./src', import.meta.url) は、その vite.config.js のURLを基準にして、
  // ./src という相対パスを解決した結果得られる、src ディレクトリの絶対URL
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server:{
    // host: true,
    // port: 5173,
    // changeOrigin: true,
    proxy:{
      '/api': {
        target: 'http://backend:5000',
      }
    },
  }

})
