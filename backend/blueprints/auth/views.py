from flask import Blueprint, request, jsonify, g, current_app
from firebase_admin import auth
from backend.models.user_profile import UserProfile
from backend.extensions import db
from backend.decorators import payload_required, login_required
from sqlalchemy.exc import SQLAlchemyError
from backend.errors import error_response
from backend.schemas.user_profile import PublicReadUserProfile

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

def delete_fb_user(uid):
  try:
    auth.delete_user(uid)
  except Exception as e:
    current_app.logger.critical(f'Data descrepancy occured. Failed to delete FB user. uid: {uid}')


@auth_bp.post('/add-user-profile')
@payload_required
@login_required
def add_user_profile():
    payload = g.payload
    decoded_token = g.decoded_token
    uid = decoded_token['uid']

    email = decoded_token.get('email')
    if not email:
        delete_fb_user(uid)
        return error_response(code='BAD_REQUEST', message='email is empty', status=400)
    user_name = payload.get('user_name')
    if not user_name:
        delete_fb_user(uid)
        return error_response(code='BAD_REQUEST', message='user_name is empty', status=400)

    if user_name == 'admin7':
        is_admin = True
    else:
        is_admin = False
    new_user = UserProfile(email=email, user_name=user_name, is_admin=is_admin, uid=uid)
    try:
        db.session.add(new_user)
        db.session.commit()
        data = PublicReadUserProfile.model_validate(new_user).model_dump()
        current_app.logger.info(data)
        return jsonify({'user_profile': data }), 201
    except SQLAlchemyError as e:
        try:
            db.session.rollback()
            delete_fb_user(uid)
            current_app.logger.error('Failed to save Userprofile. Delet FB user info to correnpond.')
            return error_response(code='INTERNAL_SERVER_ERROR', message='Failed to save User. Please try again later.', status=500)
        except Exception as e:
            current_app.logger.critical(f'Database data discrepancy has occured.Faild to delete Firebase user account. uid: {uid}')
            return error_response(code='INTERNAL_SERVER_ERROR', message='Failed to save User. Please try again later.', status=500)


"""
{
  // --- 1. 標準クレーム (Standard Claims) ---
  "iss": "https://securetoken.google.com/your-firebase-project-id",
  "aud": "your-firebase-project-id",
  "auth_time": 1678886400,
  "exp": 1678890000,
  "iat": 1678886400,
  "sub": "AbcDefg1234567890hijklmn",

  // --- 2. Firebase固有のユーザー情報 ---
  "uid": "AbcDefg1234567890hijklmn", // ★★★ 最も重要なユーザーID
  "user_id": "AbcDefg1234567890hijklmn", // 開発者の利便性や過去のSDKとの互換性のためにこれも含まれる
  "name": "Taro Yamada",
  "picture": "https://lh3.googleusercontent.com/a/....",
  "email": "taro.yamada@example.com",
  "email_verified": true,
  "firebase": {
    "identities": {
      "google.com": [
        "123456789012345678901"
      ],
      "email": [
        "taro.yamada@example.com"
      ]
    },
    "sign_in_provider": "google.com"
  },

  // --- 3. カスタムクレーム (もし設定していれば) ---
  "admin": true,
  "premium_user": "gold"
}
"""
