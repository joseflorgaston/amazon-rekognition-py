from flask import Flask, jsonify
from app.config.logging_config import logger
from app.api.routes import routes
from app.config.config import DevelopmentConfig, ProductionConfig
from flask_cors import CORS
import os

app = Flask(__name__)

# Seleccionar la configuración según el entorno
env = os.getenv('FLASK_ENV', 'development')
if env == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

# Habilitar CORS
CORS(app)

# Registrar las rutas
app.register_blueprint(routes)

# Manejador de errores global
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"An error occurred: {str(e)}", exc_info=True)
    
    response = {
        "error": "An unexpected error occurred. Please try again later."
    }
    if app.config["DEBUG"]:
        response["details"] = str(e)
    
    return jsonify(response), 500

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"])
