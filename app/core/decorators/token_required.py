from flask import current_app, request, jsonify
from app.config.mongo_client import get_mongo_client
import jwt
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')  # Usamos el request de Flask
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = get_mongo_client()["parking-lot"]["users"].find_one({'_id': data['user_id']})
        except Exception as e:
            return jsonify({'message': 'Token is invalid! {e}'}), 401
        return f(current_user, *args, **kwargs)
    return decorated
