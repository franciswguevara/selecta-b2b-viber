from flask import Blueprint

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