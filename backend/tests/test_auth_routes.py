from backend.models.user_profile import UserProfile
from sqlalchemy.exc import SQLAlchemyError
from backend.models.user_profile import UserProfile


# 成功テスト（提供されたものをベースに、ステータスコードを201に修正）
def test_add_user_profile_success(client, db_session, mock_firebase_auth):
    """
    POST /api/v1/auth/add-user-profile
    正常なリクエストでユーザープロファイルが正しく作成されることをテストする
    """
    # 1. Arrange
    test_uid = "test_user_uid_123"
    test_email = "test.user@example.com"
    mock_firebase_auth['verify_id_token'].return_value = {
        'uid': test_uid,
        'email': test_email
    }
    request_payload = {'user_name': "テストユーザー"}
    request_headers = {'Authorization': 'Bearer FAKE_ID_TOKEN'}

    # 2. Act
    response = client.post(
        '/api/v1/auth/add-user-profile',
        json=request_payload,
        headers=request_headers
    )

    # 3. Assert
    assert response.status_code == 201
    response_data = response.json
    assert 'user_profile' in response_data
    assert response_data['user_profile']['email'] == test_email
    assert response_data['user_profile']['user_name'] == "テストユーザー"

    saved_user = db_session.query(UserProfile).filter_by(uid=test_uid).one_or_none()
    assert saved_user is not None
    assert saved_user.email == test_email
    assert saved_user.user_name == "テストユーザー"
    assert saved_user.is_admin is False



def test_add_user_profile_fail_no_username(client, db_session, mock_firebase_auth):
    """
    [テストケース1: user_nameの欠落]
    リクエストボディにuser_nameが含まれない場合、400エラーが返り、
    Firebaseユーザーも削除されることをテストする
    """
    # 1. Arrange
    test_uid = "test_uid_no_username"
    test_email = "no.username@example.com"
    mock_firebase_auth['verify_id_token'].return_value = {
        'uid': test_uid,
        'email': test_email
    }
    # user_nameを含まないペイロード
    request_payload = {}
    request_headers = {'Authorization': 'Bearer FAKE_ID_TOKEN'}

    # 2. Act
    response = client.post(
        '/api/v1/auth/add-user-profile',
        json=request_payload,
        headers=request_headers
    )

    # 3. Assert
    # レスポンスの検証
    assert response.status_code == 400
    assert response.json['code'] == 'BAD_REQUEST'
    assert response.json['message'] == 'user_name is empty'

    # Firebaseユーザーが削除されたかの検証
    mock_firebase_auth['delete_user'].assert_called_once_with(test_uid)

    # DBにユーザーが保存されていないことの検証
    saved_user = db_session.query(UserProfile).filter_by(uid=test_uid).one_or_none()
    assert saved_user is None

def test_add_user_profile_fail_no_email_in_token(client, db_session, mock_firebase_auth):
    """
    [テストケース2: emailの欠落]
    FirebaseのIDトークンにemailが含まれない場合、400エラーが返り、
    Firebaseユーザーも削除されることをテストする
    """
    # 1. Arrange
    test_uid = "test_uid_no_email"
    # emailを含まないトークン情報
    mock_firebase_auth['verify_id_token'].return_value = {
        'uid': test_uid
    }
    request_payload = {'user_name': "テストユーザー"}
    request_headers = {'Authorization': 'Bearer FAKE_ID_TOKEN'}

    # 2. Act
    response = client.post(
        '/api/v1/auth/add-user-profile',
        json=request_payload,
        headers=request_headers
    )

    # 3. Assert
    assert response.status_code == 400
    assert response.json['code'] == 'BAD_REQUEST'
    assert response.json['message'] == 'email is empty'

    mock_firebase_auth['delete_user'].assert_called_once_with(test_uid)

    saved_user = db_session.query(UserProfile).filter_by(uid=test_uid).one_or_none()
    assert saved_user is None

def test_add_user_profile_fail_db_commit_error(client, db_session, mock_firebase_auth, mocker):
    """
    [テストケース3: DB保存失敗]
    データベースへのコミット時にSQLAlchemyErrorが発生した場合、500エラーが返り、
    Firebaseユーザーも削除されることをテストする
    """
    # 1. Arrange
    test_uid = "test_uid_db_error"
    test_email = "db.error@example.com"
    mock_firebase_auth['verify_id_token'].return_value = {
        'uid': test_uid,
        'email': test_email
    }
    request_payload = {'user_name': "DBエラーユーザー"}
    request_headers = {'Authorization': 'Bearer FAKE_ID_TOKEN'}

    # db.session.commit() をモックし、SQLAlchemyErrorを発生させる
    mocker.patch.object(db_session, 'commit', side_effect=SQLAlchemyError("DB commit failed"))
    # db.session.rollback() もモックしておくと、呼び出しを検証できる
    mock_rollback = mocker.patch.object(db_session, 'rollback')


    # 2. Act
    response = client.post(
        '/api/v1/auth/add-user-profile',
        json=request_payload,
        headers=request_headers
    )

    # 3. Assert
    assert response.status_code == 500
    assert response.json['code'] == 'INTERNAL_SERVER_ERROR'
    assert response.json['message'] == 'Failed to save User. Please try again later.'

    # ロールバックとFirebaseユーザー削除が呼ばれたことを確認
    mock_rollback.assert_called_once()
    mock_firebase_auth['delete_user'].assert_called_once_with(test_uid)

def test_add_user_profile_fail_duplicate_user(client, db_session, mock_firebase_auth):
    """
    [テストケース4: ユーザーの重複]
    既に同じUIDを持つユーザーがDBに存在する場合（一意性制約違反）、
    500エラーが返り、Firebaseユーザーも削除されることをテストする
    """
    # 1. Arrange
    # 事前にDBに同じUIDのユーザーを登録しておく
    test_uid = "duplicate_uid"
    test_email = "duplicate.user@example.com"
    existing_user = UserProfile(
        uid=test_uid,
        email=test_email,
        user_name="既存ユーザー",
        is_admin=False
    )
    db_session.add(existing_user)
    db_session.commit()

    # モックとリクエスト情報の設定
    mock_firebase_auth['verify_id_token'].return_value = {
        'uid': test_uid,
        'email': "new.user@example.com" # emailは変えておく
    }
    request_payload = {'user_name': "新規ユーザー"}
    request_headers = {'Authorization': 'Bearer FAKE_ID_TOKEN'}

    # 2. Act
    # 同じUIDで再度プロフィール追加を試みる
    response = client.post(
        '/api/v1/auth/add-user-profile',
        json=request_payload,
        headers=request_headers
    )

    # 3. Assert
    # SQLAlchemyErrorとして処理されるため、DBエラー時と同じ結果になる
    assert response.status_code == 500
    assert response.json['code'] == 'INTERNAL_SERVER_ERROR'

    # 新規Firebaseユーザーは削除されるはず
    mock_firebase_auth['delete_user'].assert_called_once_with(test_uid)

    # DBのユーザー数が変わっていないことを確認
    user_count = db_session.query(UserProfile).count()
    assert user_count == 1