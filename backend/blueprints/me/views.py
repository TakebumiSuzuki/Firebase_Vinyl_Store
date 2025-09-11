from flask import Blueprint, g, jsonify
from backend.decorators import login_required
from backend.models.user_profile import UserProfile
from backend.extensions import db
from backend.errors import error_response
from backend.schemas.user_profile import PublicReadUserProfile

me_bp = Blueprint('me', __name__, url_prefix='/api/v1/me')

@me_bp.get('')
@login_required
def get_me():
    decoded_token = g.decoded_token
    uid = decoded_token['uid']
    user_profile = db.session.get(UserProfile, uid)
    if not user_profile:
        return error_response('USER_NOT_FOUND', 'Could not get user', 404)
    data = PublicReadUserProfile.model_validate(user_profile).model_dump()
    return jsonify({ 'user_profile': data }), 200

