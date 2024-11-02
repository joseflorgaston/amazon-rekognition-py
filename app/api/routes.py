from flask import Blueprint
from .controllers.detect_labels_controller import detect_labels_controller
from .controllers.start_model_controller import start_model_controller
from .controllers.stop_model_controller import stop_model_controller
from .controllers.check_model_status_controller import check_model_status_controller

routes = Blueprint('routes', __name__)

# Ruta para detectar etiquetas
routes.add_url_rule('/detect-labels', 'detect_labels', detect_labels_controller, methods=['POST'])

# Rutas para iniciar y detener el modelo
routes.add_url_rule('/start-model', 'start_model', start_model_controller, methods=['POST'])
routes.add_url_rule('/stop-model', 'stop_model', stop_model_controller, methods=['POST'])

# Ruta para verificar el estado del modelo
routes.add_url_rule('/model-status', 'model_status', check_model_status_controller, methods=['GET'])
