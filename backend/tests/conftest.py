import pytest
from backend.app import create_app
from backend.extensions import db as _db
import os

@pytest.fixture(scope='session')
def app():
    """
    [部品①] テスト用のFlaskアプリケーションインスタンスを作成します。
    テスト実行中に一度だけ作成されます。
    """
    _app = create_app()

    # app_context内でappを渡すことで、テスト内でcurrent_appなどが使えるようになる
    with _app.app_context():
        yield _app

@pytest.fixture
def client(app):
    """
    [部品②] APIにリクエストを送信するためのテスト用クライアント。
    これを使ってPOSTやGETリクエストをシミュレートします。
    """
    return app.test_client()

@pytest.fixture(scope='session')
def db(app):
    """
    [部品③] テスト用のデータベースセッションを提供します。
    テスト開始時に一度だけDBテーブルを全て作成し、終了時に全て削除します。
    """
    # with app.app_context():
    _db.create_all()
    yield _db
    _db.drop_all()

@pytest.fixture(autouse=True)
def db_session(db):
    """
    [部品④] 各テストの前後でDBをクリーンな状態に保ちます。
    テストの実行後、DBに加えられた全ての変更（ユーザーの追加など）を削除します。
    これにより、各テストは常にまっさらな状態から開始できます。
    """
    yield db.session

    # --- ここから後片付け ---
    db.session.remove()
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()

@pytest.fixture
def mock_firebase_auth(mocker):
    """
    [部品⑤] Firebase Admin SDKのauthモジュールをモックに差し替えます。
    アプリケーション全体で使われるFirebase Authの呼び出しをモックします。
    """
    # --- 共通のモック ---
    # @login_required デコレーターが使用する認証チェックをモック
    mock_verify = mocker.patch('backend.decorators.verify_id_token')

    # --- 'auth' ブループリント用のモック ---
    # 元々あった、'auth'ブループリントのビューで使われる関数をモック
    # パスが存在しない場合は `mocker.patch` がエラーを出すので、実際に使われているパスにしてください
    # ここでは仮に元のパスをそのまま残します
    mock_delete_fb_user = mocker.patch('backend.blueprints.auth.views.delete_fb_user', autospec=True)

    # --- 'me' ブループリント用のモック (今回追加) ---
    # 'me'ブループリントのビューで直接 `auth` を使っている箇所をモック
    mock_update = mocker.patch('backend.blueprints.me.views.auth.update_user', autospec=True)
    mock_delete = mocker.patch('backend.blueprints.me.views.auth.delete_user', autospec=True)

    return {
        'verify_id_token': mock_verify,
        'delete_fb_user': mock_delete_fb_user, # authブループリント用
        'update_user': mock_update,           # meブループリント用
        'delete_user': mock_delete,           # meブループリント用
    }
