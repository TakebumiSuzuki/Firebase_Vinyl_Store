import { defineConfig, globalIgnores } from 'eslint/config'
import globals from 'globals'
import js from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'

// VSCodeの ESLint プラグインの自動チェックの対象は基本的にその時開いているファイルです。
// npm run lintを実行することで、プロジェクト全体のチェックができる

export default defineConfig([

  // 対象ファイルの指定
  {
    name: 'app/files-to-lint', //この設定ブロックに名前。必須ではない
    files: ['**/*.{js,mjs,jsx,vue}'], //どのファイルをESLintの対象にするか
  },

  //  チェックから除外するファイルの指定
  globalIgnores(['**/dist/**', '**/dist-ssr/**', '**/coverage/**']),

  // 実行環境の指定
  {
    languageOptions: { //言語に関する設定をまとめるプロパティ
      globals: {
        ...globals.browser,
      },
    },
  },

  js.configs.recommended, // @eslint/jsが提供する推奨ルールセットを適用

  // eslint-plugin-vue が提供する Vue.js 用のルールセットを適用。この設定セットの内部で、
  // .vueファイルを解析するために必要な vue-eslint-parser が自動的に設定されています。
  // eslint-plugin-vue をインストールすると、eslint-plugin-vue も自動でインストールされる
  ...pluginVue.configs['flat/essential'],

])
