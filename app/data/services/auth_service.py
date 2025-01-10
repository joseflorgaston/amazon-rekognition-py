
from datetime import datetime
from app.core.models.login_data import LoginData
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import jwt
from app.config.config import Config
from app.config.mongo_client import get_mongo_client
from app.interfaces.auth_interface import AuthInterface

class AuthService(AuthInterface):
    def __init__(self):
        self.db_client = get_mongo_client()
        self.user_client = self.db_client["parking-lot"]["users"]

    def login(self, login_data: LoginData):
        try:
            user = self.user_client.find_one({'username': login_data.user})
            if not user or not check_password_hash(user['password'], login_data.password):
                return jsonify({'message': 'Invalid username or password!'}), 401

            access_token = jwt.encode({
                'user_id': str(user['_id']),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, Config['SECRET_KEY'], algorithm='HS256')

            refresh_token = jwt.encode({
                'user_id': str(user['_id']),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
            }, Config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'success': True, 'access_token': access_token, 'refresh_token': refresh_token}), 200
        except (e):
            return jsonify({'success': False, 'message': 'An error occurred {e}'}), 500

    def register_user(self, login_data: LoginData):
        try:
            # Verificar si el usuario ya existe
            if self.user_client.find_one({'username': login_data.user}):
                return jsonify({'success': False, 'message': 'User already exists!'}), 400

            # Crear el hash de la contraseña
            hashed_password = generate_password_hash(login_data.password, method='pbkdf2:sha256')

            # Crear el objeto del usuario
            user = {
                'username': login_data.user,
                'password': hashed_password,
                'created_at': datetime.utcnow()
            }

            # Insertar el usuario en la base de datos
            self.user_client.insert_one(user)

            return jsonify({'success': True, 'message': 'User registered successfully!'}), 201
        except Exception as e:
            return jsonify({'success': False, 'message': f'An error occurred: {str(e)}'}), 500
        
        
    def refresh_token(self, refresh_token):
        try:
            # Decodificar el refresh token
            decoded = jwt.decode(refresh_token, Config['SECRET_KEY'], algorithms=['HS256'])
            user_id = decoded.get('user_id')

            # Verificar si el usuario existe en la base de datos
            user = self.user_client.find_one({'_id': user_id})
            if not user:
                return jsonify({'message': 'User not found!'}), 404

            # Generar un nuevo access token
            new_access_token = jwt.encode({
                'user_id': str(user['_id']),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, Config['SECRET_KEY'], algorithm='HS256')

            return jsonify({'success': True, 'access_token': new_access_token}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': 'Refresh token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': 'Invalid refresh token!'}), 401
        except Exception as e:
            return jsonify({'success': False, 'message': f'An error occurred: {str(e)}'}), 500
