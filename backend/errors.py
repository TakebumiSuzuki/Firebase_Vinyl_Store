from flask import jsonify
from firebase_admin import auth, exceptions
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, DataError, OperationalError, SQLAlchemyError
from backend.extensions import db
from werkzeug.exceptions import HTTPException


def error_response(code: str, message: str, status: int, details=None):
    payload = {"code": code, "message": message}

    # もし if details: のように書くと、値が 0や[] だったときにfalseと判定されてしまう。
    if details is not None:
        payload['details'] = details

    return jsonify(payload), status


def setup_errorhandlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        error_details = error.errors() # Pydanticのエラー詳細を取得
        app.logger.warning(f"Validation Failed: {error_details}")

        # クライアントには、どのフィールドでどのようなエラーが起きたかの詳細を返す
        return error_response(
            code='validation_error',
            message='The provided data is invalid. Please check the details.',
            status=422,
            details=error_details
        )

    # 1. IDトークンが無効、または期限切れの場合 (401 Unauthorized)
    @app.errorhandler(auth.InvalidIdTokenError)
    def handle_invalid_id_token(error):
        # このエラーは認証を必要とするエンドポイントで頻繁に発生しうる
        app.logger.info(f"Invalid ID Token received: {error}")
        return error_response(
            code='auth/invalid-token',
            message='The provided ID token is invalid, expired, or has been revoked.',
            status=401 # 認証失敗なので401が最も適切
        )

    # 2. ユーザーアカウントが無効化されている場合 (403 Forbidden)
    # @app.errorhandler(auth.DisabledAccountError)
    # def handle_disabled_account(error):
    #     app.logger.warning(f"Attempt to access with a disabled account: {error}")
    #     return error_response(
    #         code='auth/user-disabled',
    #         message='The user account has been disabled by an administrator.',
    #         status=403 # 認証はされたがアクセスが禁止されているので403が適切
    #     )

    # 3. 引数が不正な場合 (400 Bad Request)
    # @app.errorhandler(auth.InvalidArgumentError)
    # def handle_invalid_argument(error):
    #     # 例: メールアドレスの形式が不正、パスワードが弱すぎるなど
    #     app.logger.warning(f"Invalid argument provided to Firebase Auth: {error}")
    #     return error_response(
    #         code='bad_request/invalid-argument',
    #         message=f'An invalid argument was provided. {error}', # Firebaseからのエラーメッセージをそのまま含めると分かりやすい
    #         status=400 # クライアントからのリクエストが不正なので400が適切
    #     )

    @app.errorhandler(auth.UserNotFoundError)
    def handle_user_not_found(error):
        db.session.rollback()
        app.logger.warning(f"Firebase user not found: {error}")
        return error_response(code='not_found', message='The specified user was not found.', status=404)


    @app.errorhandler(auth.EmailAlreadyExistsError)
    def handle_email_already_exists(error):
        db.session.rollback()
        app.logger.warning(f"User update failed due to duplicate email.: {error}")
        return error_response(
            code='conflict/email-exists', message='The email address is already in use by another account.', status=409)

    # Firebaseとの通信エラーなどが発生した場合
    # アプリケーションが大きくなると、Firebaseの同じ機能（例えばユーザー作成）を複数の場所から呼び出すことがあります。
    # ユーザー登録画面のバグなのか、管理画面のバグなのか、バッチ処理が誤動作しているのかを究明できるようにスタックトレースを表示させる。
    @app.errorhandler(exceptions.FirebaseError)
    def handle_firebase_auth_error(error):
        db.session.rollback()
        app.logger.exception(f"Firebase Auth Error: {error}")
        return error_response(code='auth_error', message='An authentication error occurred with Firebase.', status=500)



    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error: IntegrityError):
        db.session.rollback()
        app.logger.warning(f"Database Integrity Error: {error.orig}") # .origで元のDBAPIのエラーにアクセスできます

        # 例えば、ユニークキー制約違反の場合に特化したメッセージを返すことも可能
        # if "UNIQUE constraint failed" in str(error.orig):
        #     return error_response(code='conflict/duplicate_entry', message='A record with the same value already exists.', status=409)

        return error_response(
            code='conflict/database_integrity',
            message='A database integrity constraint was violated. This may be due to a duplicate entry.',
            status=409  # 409 Conflict がより適切
        )

    @app.errorhandler(DataError)
    def handle_data_error(error: DataError):
        db.session.rollback()
        app.logger.warning(f"Database Data Error: {error.orig}")
        return error_response(
            code='bad_request/invalid_data',
            message='The provided data is not in the correct format for a database field.',
            status=400  # 400 Bad Request がより適切
        )

    # OperationalError は、DBサーバーへの接続断、認証情報の誤り、設定ミスなど、アプリケーションの動作継続に
    # 致命的な影響を与える可能性のある問題を示します。原因がアプリケーションコードのどこにあるのか、
    # あるいはインフラ側の問題なのかを切り分けるために、スタックトレースをつけるのが良い。
    @app.errorhandler(OperationalError)
    def handle_operational_error(error: OperationalError):
        db.session.rollback()
        app.logger.critical(f"Database Operational Error: {error.orig}", exc_info=True) # 接続断などはより深刻なエラー
        return error_response(
            code='service_unavailable/database',
            message='The database service is currently unavailable. Please try again later.',
            status=503  # 503 Service Unavailable がより適切
        )

    @app.errorhandler(SQLAlchemyError) # 他のSQLAlchemyエラーを捕捉
    def handle_database_error(error):
        db.session.rollback()
        app.logger.exception(f"Database Error: {error}")
        return error_response(code='database_error', message='A database error occurred.', status=500)

    # HTTPExceptionハンドラーをExceptionの直前に追加
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        # HTTPExceptionには code, name, description が含まれている
        app.logger.info(f"HTTP Exception Caught: {error.code} {error.name}")
        return error_response(
            code=error.name.lower().replace(" ", "_"), # "Not Found" -> "not_found"
            message=error.description,
            status=error.code
        )

    # 最も一般的なエラーとして最後に定義
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        db.session.rollback()
        app.logger.exception(f"An unexpected error occurred: {error}")
        return error_response(code='internal_server_error', message='An internal server error occurred.', status=500)

