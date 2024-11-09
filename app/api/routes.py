from flask import Blueprint, request
from app.api.controllers.detect_labels_controller import DetectLabelsController
from app.api.controllers.model_controller import ModelController
routes = Blueprint('routes', __name__)

@routes.route('/detect-labels', methods=['POST'])
def detect_labels():
    data = request.get_json()
    return DetectLabelsController.detect_labels(data)

@routes.route('/start-model', methods=['POST'])
def start_model():
    return ModelController.start_model()

@routes.route('/stop-model', methods=['POST'])
def stop_model():
    return ModelController.stop_model()

@routes.route('/model-status', methods=['GET'])
def model_status():
    return ModelController.model_status()