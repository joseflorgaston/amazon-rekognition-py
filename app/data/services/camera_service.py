from bson import ObjectId
from flask import jsonify
from app.config.mongo_client import get_mongo_client
from app.core.models.camera_data import CameraData
from app.interfaces.aws_rekognition_interface import RekognitionInterface

class CameraService(RekognitionInterface):
    def __init__(self):
        self.db_client = get_mongo_client()

    # Inserta una nueva camara en un parking spot en la base de datos.
    def insert_camera(self, camera: CameraData):
        try:
            camera = {
                "parking_spot_id": camera.parking_spot_id,
                "image_interval": camera.image_interval,
                "max_results": camera.max_results,
                "identifier": camera.identifier,
                "created_at": camera.created_at
            }
            result = self.db_client["parking-lot"]["cameras"].insert_one(camera)
            return jsonify({"id": str(result.inserted_id), "success": True, "message": "Camera created successfully"}), 201
        except Exception as e:
            print(f"Error al insertar la cámara: {e}")
            return jsonify({"success": False, "message": "Failed to insert camera"}), 500
    
    # Inserta una nueva camara en un parking spot en la base de datos.
    def delete_camera(self, camera_id: str):
        try:
            # Convertir image_id a ObjectId
            camera_object_id = ObjectId(camera_id)
            self.db_client["parking-lot"]["cameras"].delete_one(camera_object_id)
            return jsonify({"success": True, "message": "Camera deleted successfully"}), 201
        except Exception as e:
            print(f"Error al insertar la cámara: {e}")
            return jsonify({"success": False, "message": "Failed to delete camera"}), 500
