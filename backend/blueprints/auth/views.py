from flask import Blueprint


auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.get('/login')
def login():
    return 'helloooo'