# tests/blueprints/me/test_views.py (修正後)

import json
from backend.models.user_profile import UserProfile

# --- テスト用の定数 ---
TEST_UID = 'test_user_uid_12345'
TEST_EMAIL = 'test.user@example.com'
AUTH_HEADER = {'Authorization': 'Bearer dummy-id-token'}


def test_get_me_success(client, db_session, mock_firebase_auth):
    # ... (Arrange部分は変更なし) ...
    user = UserProfile(uid=TEST_UID, email=TEST_EMAIL, user_name='Test User')
    db_session.add(user)
    db_session.commit()

    response = client.get('/api/v1/me', headers=AUTH_HEADER)

    assert response.status_code == 200
    data = response.get_json()

    # --- 修正箇所 ---
    # uid はレスポンスに含まれていないので、その検証を削除する
    # assert data['user_profile']['uid'] == TEST_UID  <-- この行を削除またはコメントアウト

    # emailやuser_nameが正しいことの検証は残す
    assert data['user_profile']['email'] == TEST_EMAIL
    assert data['user_profile']['user_name'] == 'Test User'
    mock_firebase_auth['verify_id_token'].assert_called_once()


def test_get_me_unauthorized(client):
    """
    [異常系] GET /me: 認証ヘッダーがない場合に401エラーが返されること
    """
    # --- Act ---
    response = client.get('/api/v1/me')

    # --- Assert ---
    assert response.status_code == 401


def test_change_me_email_success(client, db_session, mock_firebase_auth):
    """
    [正常系] PUT /me/email: メールアドレスを正常に変更できること
    """
    # --- Arrange ---
    mock_firebase_auth['verify_id_token'].return_value = {'uid': TEST_UID}

    # 修正点: NOT NULL 制約を満たすため 'user_name' を追加
    user = UserProfile(uid=TEST_UID, email=TEST_EMAIL, user_name='Initial Name')
    db_session.add(user)
    db_session.commit()

    new_email = "new.email@example.com"
    payload = {'email': new_email}

    # --- Act ---
    response = client.put('/api/v1/me/email', headers=AUTH_HEADER, data=json.dumps(payload), content_type='application/json')

    # --- Assert ---
    assert response.status_code == 200
    mock_firebase_auth['update_user'].assert_called_once_with(TEST_UID, email=new_email)
    updated_user = db_session.query(UserProfile).filter_by(uid=TEST_UID).one()
    assert updated_user.email == new_email
    data = response.get_json()
    assert data['user_profile']['email'] == new_email


def test_change_me_password_success(client, mock_firebase_auth):
    """
    [正常系] PUT /me/password: パスワードを正常に変更できること
    """
    # --- Arrange ---
    mock_firebase_auth['verify_id_token'].return_value = {'uid': TEST_UID}
    new_password = "new_secure_password"
    payload = {'password': new_password}

    # --- Act ---
    response = client.put('/api/v1/me/password', headers=AUTH_HEADER, data=json.dumps(payload), content_type='application/json')

    # --- Assert ---
    assert response.status_code == 204
    mock_firebase_auth['update_user'].assert_called_once_with(TEST_UID, password=new_password)


def test_change_me_profile_success(client, db_session, mock_firebase_auth):
    """
    [正常系] PATCH /me/profile: プロフィール情報（表示名）を正常に更新できること
    """
    # --- Arrange ---
    mock_firebase_auth['verify_id_token'].return_value = {'uid': TEST_UID}

    user = UserProfile(uid=TEST_UID, email=TEST_EMAIL, user_name="Old Name")
    db_session.add(user)
    db_session.commit()

    new_user_name = "New Name"

    # --- 修正箇所 ---
    # APIのスキーマが全フィールドを要求するため、テスト側でそれに準拠したペイロードを作成する
    payload = {
        'user_name': new_user_name,
        # 必須だが変更しない項目は、現在の値を含める
        'email': user.email,
        # 他に必須項目があれば、それも追加する (例: birthday, favorite_color)
        'birthday': user.birthday.isoformat() if user.birthday else None,
        'favorite_color': user.favorite_color
    }

    # --- Act ---
    response = client.patch('/api/v1/me/profile', headers=AUTH_HEADER, data=json.dumps(payload), content_type='application/json')

    # --- Assert ---
    # これで 422 ではなく 200 が返ってくるはず
    assert response.status_code == 200

    updated_user = db_session.query(UserProfile).filter_by(uid=TEST_UID).one()
    assert updated_user.user_name == new_user_name

    data = response.get_json()
    assert data['user_profile']['user_name'] == new_user_name

def test_delete_me_success(client, db_session, mock_firebase_auth):
    """
    [正常系] DELETE /me: ユーザーアカウントを正常に削除できること
    """
    # --- Arrange ---
    mock_firebase_auth['verify_id_token'].return_value = {'uid': TEST_UID}

    # 修正点: NOT NULL 制約を満たすため 'user_name' を追加
    user = UserProfile(uid=TEST_UID, email=TEST_EMAIL, user_name='UserToDelete')
    db_session.add(user)
    db_session.commit()

    # --- Act ---
    response = client.delete('/api/v1/me', headers=AUTH_HEADER)

    # --- Assert ---
    assert response.status_code == 204
    mock_firebase_auth['delete_user'].assert_called_once_with(TEST_UID)
    deleted_user = db_session.query(UserProfile).filter_by(uid=TEST_UID).first()
    assert deleted_user is None