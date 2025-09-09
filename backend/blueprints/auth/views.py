from flask import Blueprint, request, jsonify, g
from firebase_admin.auth import verify_id_token
from backend.models.user_profile import UserProfile
from backend.extensions import db
from backend.decorators import payload_required, login_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.get('/login')
def login():
    return 'helloooo'

@auth_bp.post('/add-userporfile')
@payload_required
@login_required
def add_userprofile():
    payload = g.payload
    decoded_token = g.decoded_token

    email = payload.get('email').trim()
    if not email:
        return jsonify({'msg':'email is empty'}), 400
    user_name = payload.get('user_name').trim()
    if not user_name:
        return jsonify({'msg':'user_name is empty'}), 400

    if email == 'admin@gmail.com':
        is_admin = True
    else:
        is_admin = False

    uid = decoded_token['uid']

    new_user = UserProfile(email=email, user_name=user_name, is_admin=is_admin, uid=uid)
    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        pass

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
