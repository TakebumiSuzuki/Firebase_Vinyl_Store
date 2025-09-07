import axios from 'axios'
import { auth } from '@/firebase';

// baseURL の値が空文字列の場合、axiosはリクエストを相対パスとして扱います。つまり、リクエストは現在ブラウザで
// 表示しているページと同じオリジン（つまりViteの開発サーバー、例: http://localhost:5173）に送信されます。
// VITE_API_BASE_URL は.env.developmentに記述していないので、開発時には必ず空文字が選択される。
// import.meta.env.VITE_API_BASE_URLが実際に使われるのは、本番環境へのビルド時。ビルドすると、Vite は、
// 自動的に.env.production を環境変数に取り込み、そこに設定されている文字列に置き換えて、ビルドを生成する。
export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 10000,
})

apiClient.interceptors.request.use(
  async (config) =>{
    const user = auth.currentUser
    if (user){
      try {
        const idToken = await user.getIdToken();
        config.headers.Authorization = `Bearer ${idToken}`;
      } catch (error) {
        console.error('Could not get ID token:', error);
        // ここでエラー処理（例: ログアウトさせるなど）を行うことも可能
      }
    }
    return config
  },

  // インターセプターが実行される前の段階で、リクエスト設定に失敗した場合
  // このハンドラの主な役割は、先行する処理で発生したエラーを受け取り、それをそのまま後続の処理
  // （例えば、APIを呼び出した箇所の.catch()ブロック）に伝えることです。
  // return Promise.reject(error); と記述されているのは、エラーを握りつぶさずに正しく伝播させるための定型句。
  (error) =>{
    return Promise.reject(error);
  }

)