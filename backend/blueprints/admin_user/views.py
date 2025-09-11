from flask import Blueprint, request, jsonify, g, current_app
from firebase_admin import auth
from backend.models.user_profile import UserProfile
from backend.extensions import db
from backend.decorators import payload_required, login_required
from sqlalchemy.exc import SQLAlchemyError
from backend.errors import error_response
from backend.schemas.user_profile import PublicReadUserProfile

admin_user_bp = Blueprint('admin-user', __name__, url_prefix='/api/v1/admin-user')

@admin_user_bp.get('')
@login_required
def admin_get_users():
    pass


