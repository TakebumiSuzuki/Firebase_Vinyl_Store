import functools
from flask import request, g, jsonify, current_app
from werkzeug.exceptions import BadRequest
from firebase_admin.auth import verify_id_token, ExpiredIdTokenError, InvalidIdTokenError, RevokedIdTokenError
from backend.errors import error_response

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
        except BadRequest as e:
            return error_response(code='INVALID_PAYLOAD', message='Request body must be valid JSON with Content-Type: application/json',status=400)

        # リクエストボディが完全に空の場合、または、中身が空のJSONオブジェクト {} や空の配列 [] の場合
        if not payload:
            return error_response(
                code='EMPTY_PAYLOAD',message='Payload cannot be empty', status=400)

        g.payload = payload
        return f(*args, **kwargs)

    return wrapper



def login_required(f):
    """Decorator requiring a valid Firebase "Bearer" ID token.

        Stores decoded token in `g.decoded_token` on success, or returns 401.

        Args:
            f: The view function to protect.

        Returns:
            The decorated function.
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return error_response(
                code='AUTH_HEADER_MISSING',
                message='Authorization header is missing',
                status=401
            )
        header_parts = auth_header.split()
        if len(header_parts) != 2 or not header_parts[0].lower() == 'bearer':
            return error_response(
                code='INVALID_AUTH_HEADER_FORMAT',
                message='Invalid Authorization header format',
                status=401
            )
        id_token = header_parts[1]

        try:
            decoded_token = verify_id_token(id_token, check_revoked=True)
            
        except ExpiredIdTokenError:
            return error_response(
                code='EXPIRED_ID_TOKEN',
                message='Token has expired',
                status=401
            )
        except InvalidIdTokenError:
            return error_response(
                code='INVALID_ID_TOKEN',
                message='Invalid token',
                status=401
            )
        except RevokedIdTokenError:
            return error_response(
                code='REVOKED_ID_TOKEN',
                message='Token has been revoked',
                status=401
            )
        except Exception as e:
            # 予期せぬエラーは500エラーとして返す
            return error_response(
                code='INTERNAL_SERVER_ERROR',
                message='An unexpected error occurred',
                status=500,
                details=str(e) # エラーの詳細をdetailsに含める
            )

        g.decoded_token = decoded_token
        return f(*args, **kwargs)

    return wrapper