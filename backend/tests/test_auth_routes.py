from backend.models.user_profile import UserProfile

def test_add_user_profile_success(client, db_session, mock_firebase_auth):
    """
    POST /api/v1/auth/add-user-profile
    正常なリクエストでユーザープロファイルが正しく作成されることをテストする
    """
    # 1. Arrange (テストの準備)
    # --------------------------
    # conftestのmock_firebase_authフィクスチャを使い、
    # @login_requiredが受け取るであろうFirebaseのユーザー情報を定義
    test_uid = "test_user_uid_123"
    test_email = "test.user@example.com"
    mock_firebase_auth['verify_id_token'].return_value = {
        'uid': test_uid,
        'email': test_email
    }

    # APIに送信するリクエストボディ（ペイロード）を定義
    request_payload = {
        'user_name': "テストユーザー"
    }

    # リクエストヘッダーを定義（トークンの中身はモックしているので何でも良い）
    request_headers = {
        'Authorization': 'Bearer FAKE_ID_TOKEN'
    }

    # 2. Act (テスト対象の実行)
    # --------------------------
    # clientフィクスチャを使って、定義した情報でAPIエンドポイントにPOSTリクエストを送信
    response = client.post(
        '/api/v1/auth/add-user-profile',
        json=request_payload,
        headers=request_headers
    )

    # 3. Assert (結果の検証)
    # --------------------------
    # レスポンスが正しいか検証
    assert response.status_code == 200
    assert response.json == {'msg': 'Successfully saved user data.'}

    # データベースにユーザーが正しく保存されたか検証
    # db_sessionフィクスチャを使ってDBを直接確認
    saved_user = db_session.query(UserProfile).filter_by(uid=test_uid).one_or_none()

    assert saved_user is not None
    assert saved_user.email == test_email
    assert saved_user.user_name == "テストユーザー"
    assert saved_user.is_admin is False