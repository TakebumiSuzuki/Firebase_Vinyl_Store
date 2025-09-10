export const getErrorMessage = (error) => {
  // 1. Axiosのエラーの場合
  if (error.response) {
    // バックエンドが独自のエラーメッセージを返している場合、それを優先する
    // 例: { "message": "トークンが無効です" }
    if (error.response.data && error.response.data.message) {
      return error.response.data.message;
    }
    return `サーバーエラーが発生しました (${error.response.status})`;
  }

  // 2. Firebase Authのエラーの場合
  if (error.code) {
    switch (error.code) {
      case 'auth/user-not-found':
        return 'このメールアドレスは登録されていません。';
      case 'auth/wrong-password':
        return 'パスワードが間違っています。';
      case 'auth/invalid-email':
        return 'メールアドレスの形式が正しくありません。';
      case 'auth/too-many-requests':
        return '試行回数が上限に達しました。後ほどお試しください。';
      default:
        return '認証に失敗しました。';
    }
  }

  // 3. その他のエラー
  return '予期せぬエラーが発生しました。';
};