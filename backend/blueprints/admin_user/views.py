from flask import Blueprint, request, jsonify, g, current_app
from firebase_admin import auth
from backend.models.user_profile import UserProfile
from backend.extensions import db
from backend.decorators import payload_required, login_required, admin_required
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from backend.errors import error_response
from backend.schemas.user_profile import PublicReadUserProfile, ReadUserProfile
from datetime import datetime
from pprint import pprint

admin_user_bp = Blueprint('admin-user', __name__, url_prefix='/api/v1/admin-user')


@admin_user_bp.get('')
@login_required
@admin_required
def admin_get_users():
    stmt = select(UserProfile)
    user_profile_records = db.session.execute(stmt).scalars().all()
    user_profiles = [ReadUserProfile.model_validate(user_profile).model_dump() for user_profile in user_profile_records]

    return jsonify({'user_profiles':user_profiles}), 200


@admin_user_bp.delete('')
@payload_required
@login_required
@admin_required
def admin_delete_user():
    # アドミン自身ではなく、対象ユーザーのuidを取得している
    uid = g.payload['uid']
    auth.delete_user(uid)
    try:
        user_profile = db.session.get(UserProfile, uid)
        if not user_profile:
            return '', 204
        db.session.delete(user_profile)
        db.session.commit()

    except Exception:
        db.session.rollback()
        current_app.logger.exception(f'Database discrepancy has occured. Failed to delete user_profile of uid: {uid}')
        # この場合には、ユーザーには user_profile の消去失敗は伝える必要はないので、204でリターンをする。
    return '', 204


@admin_user_bp.get('/<string:uid>')
@login_required
@admin_required
def admin_get_user_detail(uid):

    user_profile_record = db.session.get(UserProfile, uid)
    if not user_profile_record:
        return error_response('USER_NOT_FOUND', "Coun't find the user of uid: {uid}", 500)
    unified_user_info = ReadUserProfile.model_validate(user_profile_record).model_dump()

    try:
        fb_user_record = auth.get_user(uid)
    # 通常は @app.errorhandler で補足させるが、ここに限ってはDBのデーター不整合なので、ここで補足して500番エラーで返す
    except auth.UserNotFoundError:
        current_app.logger.error(f"Data inconsistency detected: User profile exists for uid '{uid}' but user not found in Firebase.")
        return error_response('DATA_INCONSISTENCY', 'User profile exists but the corresponding Firebase user was not found.', 500)

    creation_time = datetime.fromtimestamp(fb_user_record.user_metadata.creation_timestamp / 1000)
    unified_user_info['creation_time'] = creation_time.isoformat()

    if fb_user_record.user_metadata.last_sign_in_timestamp:
        last_sign_in_time = datetime.fromtimestamp(fb_user_record.user_metadata.last_sign_in_timestamp / 1000)
        unified_user_info['last_sign_in_time'] = last_sign_in_time.isoformat()
    else:
        unified_user_info['last_sign_in_time'] = None


    return jsonify({'unified_user_info':unified_user_info}), 200














    # page_token = request.args.get('page_token')

    # # page_token の値が None の場合、最初のページ（1ページ目）のユーザーリストを返します。
    # # つまり、クライアントが page_token パラメータなしでリクエストしても、1ページ目のデータが得られる。
    # page = auth.list_users(max_results=3, page_token=page_token)

    # # user は UserRecordオブジェクト
    # users_fb_data = []
    # for user in page.users:
    #     # user.user_metadata.creation_timestamp は int型の数字データ。
    #     # Pythonのdatetimeが扱うタイムスタンプは秒単位なので、ミリ秒を秒に変換するために1000で割っている。
    #     # fromtimestampは秒単位のUnixタイムスタンプ（ただの数値）を、datetimeオブジェクトに変換するメソッドです。
    #     creation_time = datetime.fromtimestamp(user.user_metadata.creation_timestamp / 1000)
    #     last_sign_in_time = datetime.fromtimestamp(user.user_metadata.last_sign_in_timestamp / 1000)

    #     users_fb_data.append({
    #         'uid': user.uid,
    #         'email': user.email,
    #         # .isoformat()は、datetimeオブジェクトが持っている日付と時刻の情報を、ISO 8601という国際規格の文字列に変換
    #         # これは'2025-09-17T10:30:00'のような書式。FBからは当然、UTCで送られてきているので、クライアント側で時差変換が必要。
    #         'creation_timestamp': creation_time.isoformat(),
    #         'last_sign_in_timestamp': last_sign_in_time.isoformat(),
    #     })

    # next_page_token = page.next_page_token

    # return jsonify({
    #     'users_fb_data': users_fb_data,
    #     'next_page_token': next_page_token
    # }), 200


