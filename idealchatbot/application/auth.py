from flask import Blueprint, redirect, url_for, session 
from flask_login import login_required, logout_user, current_user, login_user
from .models import db, User
from . import login_manager


# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__
)

@auth_bp.route('/login', methods = ['POST'])
def login():
    pass
# Login Logic

@auth_bp.route('/signup', methods = ['POST'])
def signup():
    pass
    # Signup logic

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load"""
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    return redirect(url_for('auth_bp.login'))