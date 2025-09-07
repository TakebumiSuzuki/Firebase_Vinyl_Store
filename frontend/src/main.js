
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { onAuthStateChanged } from 'firebase/auth'
import { auth } from '@/firebase'
import App from '@/App.vue'
import { useAuthStore } from '@/stores/authStore'

// ViteやWebpackのようなビルドツールやNode.jsのモジュール解決の仕組みでは、
// ディレクトリをインポート元として指定した場合、そのディレクトリ内にあるindex.js
// （またはindex.tsなど）という名前のファイルを自動的に探して読み込む規約になっています。
// import router from './router/index.js'のように書くのと同じ
import router from '@/router'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
const authStore = useAuthStore()


let appMounted = false

onAuthStateChanged(auth, (user)=>{
  authStore.setUser(user)
  
  if (!appMounted){
    app.use(router)
    app.mount('#app')
    appMounted = true
  }
})


/*
処理の仕組み：静的解析と評価のステップ
JavaScript エンジンはモジュールを次のステップで処理します。

1. 静的解析
  ファイルを読み込むと、まず import / export を解析し、依存関係を特定します。

2.モジュールの評価
  依存するモジュール（firebase.js）が一度だけ評価されます。このとき、そのファイル内のトップレベルコード
  （例：console.log や Firebase の初期化処理）が実行されます。

3.main.js の実行
  すべての依存モジュールが評価された後、main.js の本体コードが上から順に実行されます。
  そのため、import の前後に書いた console.log よりも、firebase.js 内のログの方が先に表示されます。

.vueファイルについては、インポートされたときに、JS モジュールに変換されるが、setup() の中身はまだ実行されない。
実際に setup() が呼ばれるのは、Vue がそのコンポーネントをマウント（画面に描画）するとき。

*/
