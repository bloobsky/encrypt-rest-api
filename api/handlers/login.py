from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from api.conf import MONGODB_HOST, MONGODB_PORT, MONGODB_DBNAME
from api.crypto_utils import check_password
from uuid import uuid4
from datetime import datetime, timedelta

login_bp = Blueprint('login', __name__, url_prefix='/students/api')

client = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client[MONGODB_DBNAME]


@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').lower().strip()
    password = data.get('password', '')

    user = db.users.find_one({'email': email})
    if not user:
        return jsonify({"message": "Invalid credentials!"}), 403

    if not check_password(password, user['password'], user['salt']):
        return jsonify({"message": "Invalid credentials!"}), 403

    token = uuid4().hex
    expires = datetime.utcnow() + timedelta(hours=2)
    expires_ts = int(expires.timestamp())

    db.users.update_one({'email': email}, {
                        '$set': {'token': token, 'expiresIn': expires_ts}})

    return jsonify({"token": token, "expiresIn": expires_ts}), 200
