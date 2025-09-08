from flask import Flask
from backend.extensions import db, migrate
import os
from backend.config import configs_dic
import firebase_admin
from firebase_admin import credentials

def createApp():
    app = Flask(__name__)


    if os.getenv('TEST_MODE'): #これは docker-compose.test.ymlファイルで指定される
        config_class = configs_dic['testing']
    else:
        config_class = configs_dic['development']

    app.config.from_object(config_class)


    fb_key_path = app.config.get('FIREBASE_SERVICE_ACCOUNT_KEY_PATH')
    if fb_key_path:
        try:
            # アプリがすでに初期化されていないかチェック
            if not firebase_admin._apps:
                cred = credentials.Certificate(fb_key_path)
                # firebase_admin.initialize_app(cred) により _apps辞書に「デフォルトアプリ」が登録されます
                # firebase_adminモジュール自体が、内部の _apps 辞書を通して初期化されたAppオブジェクトへの参照を保持・管理してくれる
                # auth, firestore, storage などのサブモジュールは、_apps 辞書に登録されている "[DEFAULT]" のAppを自動的に見つけて利用する
                firebase_admin.initialize_app(cred)
                app.logger.info("Firebase Admin SDKが正常に初期化されました。")

        except (FileNotFoundError, ValueError) as e:
            # パスは設定されているが、ファイルがない、または中身が不正な場合のエラーハンドリング
            app.logger.critical(f"Firebase Admin SDKの初期化に失敗しました: {e}")
            raise SystemExit("アプリケーションを起動できません。Firebaseの認証設定を確認してください。")
    else:
        #テストの場合にはfirebaseのキーを環境変数として設定しないのでここにくる
        # 設定がない場合は、その旨をログに出力しておくと親切
        app.logger.warning("FIREBASE_SERVICE_ACCOUNT_KEY_PATHが設定されていません。Firebaseの初期化をスキップします。")


    db.init_app(app)
    migrate.init_app(app, db)




    return app

