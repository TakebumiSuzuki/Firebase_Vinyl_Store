import functools
from flask import request, g, jsonify, current_app
from werkzeug.exceptions import BadRequest
from firebase_admin.auth import verify_id_token, ExpiredIdTokenError, InvalidIdTokenError, RevokedIdTokenError

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
        current_app.logger.info('PAYLOAD1')
        try:
            payload = request.get_json()

        # Content-Type が application/json でない場合や、JSONの構文が間違っている場合
        except BadRequest as e:
            return jsonify({'msg':'Request body must be valid JSON with Content-Type: application/json'}), 400
        current_app.logger.info('PAYLOAD2')
        # リクエストボディが完全に空の場合、または、中身が空のJSONオブジェクト {} や空の配列 [] の場合
        if not payload:
            return jsonify({'msg':'Payload cannot be empty'}), 400

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
        current_app.logger.info('LOGIN')

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Authorization header is missing'}), 401
        current_app.logger.info('LOGIN')
        header_parts = auth_header.split()
        if len(header_parts) != 2 or not header_parts[0].lower() == 'bearer':
            return jsonify({'message': 'Invalid Authorization header format'}), 401
        id_token = header_parts[1]
        current_app.logger.info('LOGIN')
        try:
            decoded_token = verify_id_token(id_token, check_revoked=True)
        except ExpiredIdTokenError as e:
            return jsonify({'message': 'Token has expired'}), 401
        except InvalidIdTokenError as e:
            return jsonify({'message': 'Invalid token'}), 401
        # check_revoked=Trueにより、このエラーが発生する可能性が追加される
        except RevokedIdTokenError as e:
            return jsonify({'message': 'Token has been revoked'}), 401
        except Exception as e:
            return jsonify({'message': f'An unexpected error occurred: {e}'}), 500

        g.decoded_token = decoded_token
        return f(*args, **kwargs)

    return wrapper