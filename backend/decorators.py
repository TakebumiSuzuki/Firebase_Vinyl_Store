import functools
from flask import request, g, jsonify, current_app
from werkzeug.exceptions import BadRequest
from firebase_admin.auth import verify_id_token, ExpiredIdTokenError, InvalidIdTokenError, RevokedIdTokenError
from backend.errors import error_response
from backend.extensions import db
from backend.models.user_profile import UserProfile

def payload_required(f):
    """Requires a non-empty JSON payload in the request.

    Verifies 'application/json' Content-Type and a non-empty body.
    On success, stores payload in `g.payload`; otherwise, returns a 400 error.

    Args:
        f (Callable): The view function to decorate.

    Returns:
        Callable: The decorated function.

    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            payload = request.get_json()

        # Content-Type が application/json でない場合や、JSONの構文が間違っている場合
        except BadRequest as error:
            current_app.logger.error(f'Request body must be valid JSON with Content-Type: application/json: {error}')
            return error_response(
                code='INVALID_PAYLOAD',
                message='Request body must be valid JSON with Content-Type: application/json',
                status=400
            )

        # リクエストボディが完全に空の場合、または、中身が空のJSONオブジェクト {} や空の配列 [] の場合
        if not payload:
            current_app.logger.error(f'Payload is empty.')
            return error_response(
                code='EMPTY_PAYLOAD',
                message='Payload cannot be empty',
                status=400
            )

        g.payload = payload
        return f(*args, **kwargs)

    return wrapper



def login_required(f):
    """Decorator requiring a valid Firebase "Bearer" ID token.

        Stores decoded token in `g.decoded_token` adn uid in 'g.uid' on success, or returns 401.

        Args:
            f: The view function to protect.

        Returns:
            The decorated function.
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            current_app.logger.error(f'Authorization header is missing.')
            return error_response(
                code='AUTH_HEADER_MISSING',
                message='Authorization header is missing',
                status=401
            )
        header_parts = auth_header.split()
        if len(header_parts) != 2 or not header_parts[0].lower() == 'bearer':
            current_app.logger.error(f'Invalid Authorization header format.')
            return error_response(
                code='INVALID_AUTH_HEADER_FORMAT',
                message='Invalid Authorization header format',
                status=401
            )
        id_token = header_parts[1]

        try:
            # passwordの変更の際には、Firebase Authは自動的に、auth.revoke_refresh_tokens(uid)をおこなってくれる。
            # ユーザー情報の tokensValidAfterTime に現在時刻が設定されるが、これだけだとトークンの Refresh時にしか効力がない。
            # check_revoked=True とすると、IDトークンに刻まれた発行時刻が、tokensValidAfterTime よりも後であることを確認する。
            # これにより、デバイス全部が一気にログイン必要となる。
            decoded_token = verify_id_token(id_token, check_revoked=True)

        except ExpiredIdTokenError:
            current_app.logger.warning(f'Token has expired')
            return error_response(
                code='EXPIRED_ID_TOKEN',
                message='Token has expired',
                status=401
            )
        except InvalidIdTokenError:
            current_app.logger.warning(f'Invalid token')
            return error_response(
                code='INVALID_ID_TOKEN',
                message='Invalid token',
                status=401
            )
        except RevokedIdTokenError:
            current_app.logger.warning(f'Token has been revoked')
            return error_response(
                code='REVOKED_ID_TOKEN',
                message='Token has been revoked',
                status=401
            )
        except Exception as error:
            current_app.logger.exception(f'An unexpected error occurred: {error}')
            # 予期せぬエラーは500エラーとして返す
            return error_response(
                code='INTERNAL_SERVER_ERROR',
                message='An unexpected error occurred',
                status=500,
                details=str(error) # エラーの詳細をdetailsに含める
            )

        g.decoded_token = decoded_token
        g.uid = decoded_token['uid']
        return f(*args, **kwargs)

    return wrapper


def user_profile_required(f):
    """Requires and loads the user profile for the authenticated user.

    - Must be used after `@login_required`.
    - Attaches the `UserProfile` object to `g.user_profile_record`.
    - Returns 404 if the profile is not found.
    - Returns 500 if the decorator is used incorrectly.

    Args:
        f (Callable): The view function to decorate.

    Returns:
        Callable: The decorated function.
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not hasattr(g, 'uid'):
            current_app.logger.exception("The g proxy object for this app context doesn't have uid key.")
            return error_response(
                code='USER_PROFILE_NOT_FOUND',
                message="Couldn't find user_profile for this user.",
                status=500
            )
        user_profile = db.session.get(UserProfile, g.uid)
        if not user_profile:
            current_app.logger.exception(f"Couldn't find user_profile for this uid: {g.uid}")
            return error_response(
                code='USER_PROFILE_NOT_FOUND',
                message="Couldn't find user_profile for this user.",
                status=404
            )
        g.user_profile_record = user_profile

        return f(*args, **kwargs)

    return wrapper