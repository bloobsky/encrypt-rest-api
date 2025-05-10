from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from api.conf import MONGODB_HOST, MONGODB_PORT, MONGODB_DBNAME
from api.crypto_utils import decrypt

user_bp = Blueprint('user', __name__, url_prefix='/students/api')

client = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client[MONGODB_DBNAME]

@user_bp.route('/user', methods=['GET'])
def get_user():
    token = request.headers.get('X-Token')
    if not token:
        return jsonify({ "message": "Token missing!" }), 400

    user = db.users.find_one({ 'token': token })
    if not user or 'expiresIn' not in user:
        return jsonify({ "message": "Invalid or expired token!" }), 403

    result = {
        'email': user['email'],
        'displayName': decrypt(user.get('displayName', '')),
        'address': decrypt(user.get('address', '')),
        'phone': decrypt(user.get('phone', '')),
        'dateOfBirth': decrypt(user.get('dateOfBirth', '')),
        'disabilities': decrypt(user.get('disabilities', ''))
    }

    return jsonify(result), 200
