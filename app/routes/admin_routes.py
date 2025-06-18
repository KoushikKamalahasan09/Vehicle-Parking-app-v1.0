from flask import Blueprint,render_template,flash
from app.utils.decorators import login_required, admin_required
from app.models import User


bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
@admin_required
def admin_dashboard():
    flash("Welcome to the admin dashboard!")
    return render_template('admin/dashboard.html')