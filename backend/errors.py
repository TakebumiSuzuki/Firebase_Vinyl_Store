from flask import jsonify

def error_response(code: str, message: str, status: int, details=None):

    payload = {"code": code, "message": message}

    # もし if details: のように書くと、値が 0や[] だったときにfalseと判定されてしまう。
    if details is not None:
        payload['details'] = details

    return jsonify(payload), status