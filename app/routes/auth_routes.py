from flask import Blueprint,flash,render_template
from app.utils.decorators import login_required, admin_required
from app.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login')
def login():
    return render_template('auth/login.html')