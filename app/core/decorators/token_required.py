from flask import current_app, request, jsonify
from app.config.mongo_client import get_mongo_client
import jwt
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')  # Buscar en Authorization
        if not auth_header:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Extraer el token del formato "Bearer <token>"
            token = auth_header.split(" ")[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = get_mongo_client()["parking-lot"]["users"].find_one({'_id': data['user_id']})
        except IndexError:
            return jsonify({'message': 'Token is missing or invalid format!'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        except Exception as e:
            return jsonify({'message': f'An error occurred: {str(e)}'}), 500

        return f(current_user, *args, **kwargs)

    return decorated
