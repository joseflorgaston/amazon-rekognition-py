from flask import Blueprint, request
from app.api.controllers.aws_controller import AWSController
from app.api.controllers.model_controller import ModelController
from app.api.controllers.parking_lot_controller import ParkingLotController
routes = Blueprint('routes', __name__)

@routes.route('/detect-labels', methods=['POST'])
def detect_labels():
    data = request.get_json()
    return ModelController.detect_labels(data)

@routes.route('/start-model', methods=['POST'])
def start_model():
    return ModelController.start_model()

@routes.route('/stop-model', methods=['POST'])
def stop_model():
    return ModelController.stop_model()

@routes.route('/model-status', methods=['GET'])
def model_status():
    return ModelController.model_status()

@routes.route('/upload-image', methods=['POST'])
def upload_image():
    data = request.get_json()
    return AWSController.upload_image(data)

@routes.route('/create-parking-spot', methods=['POST'])
def insert_parking_spot():
    data = request.get_json()
    return ParkingLotController.insert_parking_spot(data)

@routes.route('/create-camera', methods=['POST'])
def insert_camera():
    data = request.get_json()
    return ParkingLotController.insert_camera(data)

@routes.route('/create-image', methods=['POST'])
def insert_image():
    data = request.get_json()
    return ParkingLotController.insert_image(data)
