import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Viteは、.envファイルに記述された変数のうち、VITE_というプレフィックスが付いているものだけをクライアントサイドのコードに公開(埋め込み)します
// import.meta.envは、Viteが提供するECMAScript標準に沿った方法で環境変数にアクセスするための仕組みです。

// Viteのビルドプロセスは、コード内の import.meta.env.VITE_XXX という記述を見つけると、.env ファイルに書かれている実際の値に置き換えて、
// 最終的なJavaScriptファイル（静的ファイル）を生成します。
// こうやって埋め込まれた環境変数の値はブラウザの開発者ツールを使えば、エンドユーザーは誰でもその値を見ることができます。が、問題なし。
// メリットとしては、複数の場所からこれらの値にアクセスしたり、.env自体を切り替えたりできる。.gitignoreには入れておくことが推奨される。

// また、Viteのデフォルトの動作として、実行するコマンドに応じて自動的に読み込む .env ファイルを切り替えてくれます。
// vite (または vite dev, vite serve) を実行した場合、.env.development ファイルを優先的に読み込みます。
// vite build を実行した場合は .env.production ファイルを優先的に読み込みます。

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
// この時点では、auth.currentUser は null です。
console.log('FB authがイニシャライズされた直後のcurrentUser',auth.currentUser); // null

export { auth }


/*
getAuth(app) を呼ぶと、以下が非同期で行われる。

1. ストレージの復元処理
- IndexedDB / LocalStorage / SessionStorage からトークンやユーザー情報を探し出し、利用可能なセッションがあれば復元を開始します。
* ここでは、IDトークンの有効期限チェックは行われない。トークンのリフレッシュなども getAuth メソッドでは行われないことに注意！

2. auth.currentUser の更新
- ユーザー情報が取得されると、auth.currentUser が更新されます。
- この後、必要に応じてイベント（onAuthStateChanged や onIdTokenChanged）が発火します。

*/