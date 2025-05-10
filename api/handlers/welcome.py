from flask import Blueprint, jsonify

welcome_bp = Blueprint('welcome', __name__, url_prefix='/students/api')

@welcome_bp.route('/', methods=['GET'])
def welcome():
    return jsonify({ "message": "Welcome to the Cyber Students Server!" }), 200
