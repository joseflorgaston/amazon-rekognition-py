import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

class Config:
    """Configuración base (general para todos los entornos)"""
    DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION')
    PROJECT_ARN = os.getenv('PROJECT_ARN')
    SECRET_KEY = os.getenv('SECRET_KEY')
    MODEL_ARN = os.getenv('MODEL_ARN')
    MIN_INFERENCE_UNITS = int(os.getenv('MIN_INFERENCE_UNITS', 1))
    VERSION_NAME = os.getenv('VERSION_NAME')
    PARKING_LOT_BUCKET_ARN = os.getenv('PARKING_LOT_BUCKET_ARN')
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    MONGODB_URI = os.getenv('MONGODB_URI')

class DevelopmentConfig(Config):
    """Configuración específica para el entorno de desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración específica para el entorno de producción"""
    DEBUG = False
