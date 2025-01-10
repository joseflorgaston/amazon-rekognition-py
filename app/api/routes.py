from app.api.controllers.auth_controller import AuthController
from app.core.decorators import token_required
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

@routes.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    return AuthController.login(data)

@routes.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    return AuthController.register_user(data)

# Ruta para refrescar el token de acceso
@routes.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    return AuthController.refresh(data)

@routes.route('/model/start', methods=['POST'])
def start_model():
    return ModelController.start_model()

@routes.route('/model/stop', methods=['POST'])
def stop_model():
    return ModelController.stop_model()

@routes.route('/model/status', methods=['GET'])
def model_status():
    return ModelController.model_status()

@routes.route('/parking_spot', methods=['GET'])
def get_parking_spots():
    return ParkingSpotController.get_parking_spots()

@routes.route('/parking_spot/<parking_spot_id>', methods=['GET'])
def get_parking_spot(parking_spot_id):
    return ParkingSpotController.get_parking_spot(parking_spot_id)

@routes.route('/parking_spot/create', methods=['POST'])
def insert_parking_spot():
    data = request.get_json()
    return ParkingSpotController.insert_parking_spot(data)

@routes.route('/parking_spot/update/<parking_spot_id>', methods=['PUT'])
def update_parking_spot(parking_spot_id):
    data = request.get_json()
    return ParkingSpotController.update_parking_spot(parking_spot_id, data)

@routes.route('/parking_spot/<parking_spot_id>', methods=['DELETE'])
def delete_parking_spot(parking_spot_id):
    return ParkingSpotController.delete_parking_spot(parking_spot_id)

@routes.route('/parking_spot/cameras/<parking_spot_id>', methods=['GET'])
def get_parking_spot_cameras(parking_spot_id: str):
    return CameraController.get_parking_spot_cameras(parking_spot_id)

@routes.route('/camera', methods=['GET'])
def get_cameras():
    return CameraController.get_cameras()

@routes.route('/camera/create', methods=['POST'])
def insert_camera():
    data = request.get_json()
    return CameraController.insert_camera(data)

@routes.route('/camera/update/<camera_id>', methods=['PUT'])
def update_camera(camera_id):
    data = request.get_json()
    return CameraController.update_camera(camera_id, data)

@routes.route('/camera/update_image_interval/<camera_id>', methods=['PATCH'])
def update_camera_image_interval(camera_id):
    data = request.get_json()
    return CameraController.update_camera_image_interval(camera_id, data)

@routes.route('/camera/update_max_results/<camera_id>', methods=['PATCH'])
def update_camera_max_results(camera_id):
    data = request.get_json()
    return CameraController.update_camera_max_results(camera_id, data)

@routes.route('/camera/<camera_id>', methods=['DELETE'])
def delete_camera(camera_id):
    print(camera_id)
    return CameraController.delete_camera(camera_id)

@routes.route('/image/<camera_id>', methods=['GET'])
def get_last_image(camera_id):
    return ImageController.get_last_image(camera_id)

@routes.route('/image/create', methods=['POST'])
def insert_image():
    data = request.get_json()
    return ImageController.insert_image(data)

@routes.route('/image/upload', methods=['POST'])
def upload_image():
    data = request.get_json()
    return AWSController.upload_image(data)

@routes.route('/image/<image_id>', methods=['DELETE'])
def deleteImage(image_id):
    return ImageController.delete_image(image_id)
