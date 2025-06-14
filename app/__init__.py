# app/__init__.py

from flask import Flask
from .models import db, User
from werkzeug.security import generate_password_hash

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        db.create_all()

        # Create default admin
        admin = User.query.filter_by(is_admin=True).first()
        if not admin:
            admin = User(
                username='admin',
                passhash=generate_password_hash('admin123'),
                email='admin@parkingapp.com',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()

    # Register routes here...
    from app.routes import auth_routes, admin_routes, users_routes, summary_routes
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(admin_routes.bp)
    app.register_blueprint(users_routes.bp)
    app.register_blueprint(summary_routes.bp)

    return app
