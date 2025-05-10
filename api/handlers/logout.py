from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from api.conf import MONGODB_HOST, MONGODB_PORT, MONGODB_DBNAME

logout_bp = Blueprint('logout', __name__, url_prefix='/students/api')

client = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client[MONGODB_DBNAME]


@logout_bp.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('X-Token')
    if not token:
        return jsonify({"message": "Token missing!"}), 400

    result = db.users.update_one({'token': token}, {'$set': {'token': None}})
    if result.matched_count == 0:
        return jsonify({"message": "Invalid or expired token!"}), 403

    return jsonify({"message": "Logged out successfully."}), 200
