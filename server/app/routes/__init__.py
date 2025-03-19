from flask import Blueprint

# Create a global blueprint for the app
main_bp = Blueprint('main', __name__)

# Import all route modules (ensures they get registered)
