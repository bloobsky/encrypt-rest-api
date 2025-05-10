from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from api.conf import MONGODB_HOST, MONGODB_PORT, MONGODB_DBNAME
from api.crypto_utils import hash_password, encrypt

registration_bp = Blueprint('registration', __name__, url_prefix='/students/api')

client = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client[MONGODB_DBNAME]

@registration_bp.route('/registration', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email', '').lower().strip()
    password = data.get('password', '')
    display_name = data.get('displayName', email)
    address = data.get('address', '')
    phone = data.get('phone', '')
    dob = data.get('dateOfBirth', '')
    disabilities = ','.join(data.get('disabilities', []))

    if not email or not password:
        return jsonify({ "message": "Missing required fields!" }), 400

    if db.users.find_one({ 'email': email }):
        return jsonify({ "message": "User already exists!" }), 409

    hashed, salt = hash_password(password)

    db.users.insert_one({
        'email': email,
        'password': hashed,
        'salt': salt,
        'displayName': encrypt(display_name),
        'address': encrypt(address),
        'phone': encrypt(phone),
        'dateOfBirth': encrypt(dob),
        'disabilities': encrypt(disabilities)
    })

    return jsonify({ "email": email, "displayName": display_name }), 200
