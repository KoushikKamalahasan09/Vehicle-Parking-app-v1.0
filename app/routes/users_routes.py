from flask import Blueprint,flash,render_template,redirect,url_for,session
from app.utils.decorators import login_required, admin_required
from app.models import User

bp = Blueprint('user', __name__)

@bp.route('/<username>/dashboard')
@login_required
def user_dashboard(username):
    if username != session.get('username'):
        session.pop('username', None)
        flash("You are not authorized to view this page. You are being logged out.")
        return redirect(url_for('auth.login'))
    flash(f"Welcome to your dashboard, {username}!")
    return render_template('user/dashboard.html')