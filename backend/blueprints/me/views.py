from flask import Blueprint, g, jsonify, current_app
from firebase_admin import auth
from backend.decorators import login_required, payload_required, user_profile_required
from backend.models.user_profile import UserProfile
from backend.extensions import db
from backend.errors import error_response
from backend.schemas.user_profile import PublicReadUserProfile, UpdateUserProfile, ChangeEmailSchema

me_bp = Blueprint('me', __name__, url_prefix='/api/v1/me')

@me_bp.get('')
@login_required
@user_profile_required
def get_me():
    user_profile_record = g.user_profile_record
    user_profile_dic = PublicReadUserProfile.model_validate(user_profile_record).model_dump()
    return jsonify({ 'user_profile': user_profile_dic }), 200


# FB Authで、メールアドレスを変更しただけでは、リフレッシュトークンは自動的に失効しない。
# つまり、auth.revoke_refresh_tokens(uid)は呼ばれない.
@me_bp.put('/email')
@payload_required
@login_required
@user_profile_required
def change_me_email():
    dto = ChangeEmailSchema.model_validate(g.payload)
    new_email = dto.email

    uid = g.uid
    auth.update_user(uid, email=new_email)
    try:
        user_profile_record = g.user_profile_record
        user_profile_record.email = new_email
        db.session.commit()
        user_profile_dic = PublicReadUserProfile.model_validate(user_profile_record).model_dump()
        return jsonify({'user_profile': user_profile_dic}), 200

    except Exception as e:
        current_app.logger.exception(f"Database discrepancy occured. Failed to update email in UserProfile, uid: {uid} - {e}")
        raise


# パスワードが変更された場合、Firebase Authenticationは自動的にそのユーザーの既存のリフレッシュトークンを
# すべて失効させます。つまり、内部的に、auth.revoke_refresh_tokens(uid)が自動で実行される。これは、
# Firebaseの内部のユーザー情報の tokensValidAfterTime というタイムスタンプに現在の時刻を記録する。
# これにより、全ての端末が、最長で１時間後にはリフレッシュできなくなる。しかし、もし即座にアクセス不能にしたければ、
#　login_required のデコレーター内で　verify_id_token(id_token, check_revoked=True)　とする。
@me_bp.put('/password')
@login_required
@payload_required
def change_me_password():
    uid = g.uid
    payload = g.payload
    if 'password' not in payload:
        current_app.logger.warning('')
        return error_response('NO_PASSWORD_IN_PAYLOAD', 'Password should be in the payload', 400)
    new_password = payload['password']
    auth.update_user(uid, password=new_password)
    return jsonify(''), 204


@me_bp.patch('/profile')
@login_required
@payload_required
@user_profile_required
def change_me_profile():
    payload = g.payload
    updates = UpdateUserProfile.model_validate(payload).model_dump(exclude_unset=True)

    user_profile_record = g.user_profile_record
    for key, value in updates.items():
        setattr(user_profile_record, key, value)
    db.session.commit()
    user_profile_dic = PublicReadUserProfile.model_validate(user_profile_record).model_dump()
    return jsonify({ 'user_profile': user_profile_dic }), 200


@me_bp.delete('')
@login_required
@user_profile_required
def delete_me():
    uid = g.uid
    auth.delete_user(uid)

    try:
        user_profile_record = g.user_profile_record
        db.session.delete(user_profile_record)
        db.session.commit()
        return '', 204
    except Exception as e:
        current_app.logger.exception(f'Database discrepancy has occured. Failed to delete user_profile for this user: {uid} - {e}')
        # raise によって元のエラー (IntegrityErrorなど) をそのまま再スローする。
        raise


"""
user = auth.update_user(uid, email=new_email)などで Firebase Auth から戻ってくる user は
UserRecordオブジェクト。その属性を辞書のように書くと。。
注意点としては、このアプリではuid, email 以外は使っていないということ。
{
    "uid": "ユーザーの一意なID (文字列)",
    "email": "メールアドレス (文字列, オプション)",
    "email_verified": "メールアドレスが確認済みかどうか (ブール値)",
    "display_name": "表示名 (文字列, オプション)",
    "photo_url": "プロフィール写真のURL (文字列, オプション)",
    "phone_number": "電話番号 (文字列, オプション)",
    "disabled": "アカウントが無効化されているかどうか (ブール値)",
    "user_metadata": {
        "creation_timestamp": "アカウント作成日時 (タイムスタンプ)",
        "last_sign_in_timestamp": "最終サインイン日時 (タイムスタンプ, オプション)"
    },
    "provider_data": [
        {
            "provider_id": "プロバイダーID (例: 'password', 'google.com')",
            "uid": "そのプロバイダーにおけるユーザーID (文字列)",
            "display_name": "プロバイダーの表示名 (文字列, オプション)",
            "email": "プロバイダーのメールアドレス (文字列, オプション)",
            "photo_url": "プロバイダーのプロフィール写真URL (文字列, オプション)"
        }
        # ... 連携しているプロバイダーの数だけ続く
    ],
    "custom_claims": "カスタムクレーム (辞書, オプション)",
    "tokens_valid_after_timestamp": "トークンの有効期限を示すタイムスタンプ (タイムスタンプ, オプション)"
}

"""
