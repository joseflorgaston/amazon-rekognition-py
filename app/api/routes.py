from flask import Blueprint, request
from app.api.controllers.aws_controller import AWSController
from app.api.controllers.camera_controller import CameraController
from app.api.controllers.image_controller import ImageController
from app.api.controllers.model_controller import ModelController
from app.api.controllers.parking_spot_controller import ParkingSpotController
routes = Blueprint('routes', __name__)

@routes.route('/detect_labels', methods=['POST'])
def detect_labels():
    data = request.get_json()
    return ModelController.detect_labels(data)

@routes.route('/start_model', methods=['POST'])
def start_model():
    return ModelController.start_model()

@routes.route('/stop_model', methods=['POST'])
def stop_model():
    return ModelController.stop_model()

@routes.route('/model_status', methods=['GET'])
def model_status():
    return ModelController.model_status()

@routes.route('/upload_image', methods=['POST'])
def upload_image():
    data = request.get_json()
    return AWSController.upload_image(data)

@routes.route('/create_parking_spot', methods=['POST'])
def insert_parking_spot():
    data = request.get_json()
    return ParkingSpotController.insert_parking_spot(data)

@routes.route('/delete_parking_spot/<parking_spot_id>', methods=['DELETE'])
def delete_parking_spot(parking_spot_id):
    return ParkingSpotController.delete_parking_spot(parking_spot_id)

@routes.route('/create_camera', methods=['POST'])
def insert_camera():
    data = request.get_json()
    return CameraController.insert_camera(data)

@routes.route('/delete_camera/<camera_id>', methods=['DELETE'])
def delete_camera(camera_id):
    return CameraController.delete_camera(camera_id)

@routes.route('/create_image', methods=['POST'])
def insert_image():
    data = request.get_json()
    return ImageController.insert_image(data)

@routes.route('/delete_image/<image_id>', methods=['DELETE'])
def deleteImage(image_id):
    return ImageController.delete_image(image_id)
