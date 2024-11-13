from pymongo import MongoClient
from flask import current_app

def get_mongo_client():
    """Obtiene el cliente de MongoDB configurado desde las variables de entorno"""
    client = MongoClient(current_app.config['MONGODB_URI'])
    return client
