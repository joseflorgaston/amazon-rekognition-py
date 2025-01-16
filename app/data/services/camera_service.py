from bson import ObjectId
from flask import jsonify
from app.config.mongo_client import get_mongo_client
from app.core.models.camera_data import CameraData
from app.interfaces.camera_interface import CameraInterface

class CameraService(CameraInterface):
    def __init__(self):
        self.db_client = get_mongo_client()
        self.camera_client = self.db_client["parking-lot"]["cameras"]
        self.parking_spot_client = self.db_client["parking-lot"]["parking_spot"]

    # Retorna las cámaras guardadas en la base de datos junto con sus parking spots
    def get_cameras(self):
        try:
            result = self.camera_client.find()
            cameras = list(result)

            enriched_cameras = []
            for camera in cameras:
                camera["_id"] = str(camera["_id"])
                camera["parking_spot_id"] = str(camera["parking_spot_id"])

                parking_spot = self.parking_spot_client.find_one({"_id": ObjectId(camera["parking_spot_id"])})
                if parking_spot:
                    parking_spot["_id"] = str(parking_spot["_id"])
                    camera["parking_spot"] = parking_spot
                else:
                    # Si no se encuentra el parking spot, agregar un valor por defecto
                    camera["parking_spot"] = None

                enriched_cameras.append(camera)

            return jsonify({"data": enriched_cameras, "success": True, "message": "Cameras retrieved successfully"}), 200
        except Exception as e:
            print(f"Error retrieving cameras: {e}")
            return jsonify({"success": False, "message": "Failed to retrieve cameras"}), 500

    # Retorna las camaras de un parking spot guardadas en la base de datos.
    def get_parking_spot_cameras(self, parking_spot_id: str):
        try:
            # Convert parking_spot_id to ObjectId
            parking_spot_object_id = ObjectId(parking_spot_id)

            # Query the database for cameras associated with the parking spot
            result = self.camera_client.find({"parking_spot_id": parking_spot_object_id})

            # Convert the result to a list and serialize ObjectId for JSON response
            cameras = list(result)
            for camera in cameras:
                camera["_id"] = str(camera["_id"])
                camera["parking_spot_id"] = str(camera["parking_spot_id"])

            return jsonify({"data": cameras, "success": True, "message": "Cameras retrieved successfully"}), 200
        except Exception as e:
            print(f"Error retrieving cameras: {e}")
            return jsonify({"success": False, "message": "Failed to retrieve cameras"}), 500

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
            result = self.camera_client.insert_one(camera)
            return jsonify({"id": str(result.inserted_id), "success": True, "message": "Camera created successfully"}), 201
        except Exception as e:
            print(f"Error al insertar la cámara: {e}")
            return jsonify({"success": False, "message": "Failed to insert camera"}), 500

    # Actualiza una camara en la base de datos.
    def update_camera(self, camera_id: str, camera: CameraData):
        try:
            camera_object_id = ObjectId(camera_id)
            camera = {
                "parking_spot_id": ObjectId(camera.parking_spot_id),
                "image_interval": camera.image_interval,
                "max_results": camera.max_results,
                "identifier": camera.identifier,
                "created_at": camera.created_at
            }
            # Realizar la actualización en la base de datos
            self.camera_client.find_one_and_update(
                {"_id": camera_object_id},
                {"$set": camera},
                return_document=True
            )

            return jsonify({"success": True, "message": "Camera updated successfully"}), 201
        except Exception as e:
            print(e)
            return jsonify({"success": False, "message": "Failed to update camera"}), 500

    # Update only the max_results of the camera in the database
    def update_camera_max_results(self, camera_id: str, max_results: int):
        try:
            camera_object_id = ObjectId(camera_id)
            result = self.camera_client.update_one(
                {"_id": camera_object_id},
                {"$set": {"max_results": max_results}}
            )

            if result.matched_count == 0:
                return jsonify({"success": False, "message": "Camera not found"}), 404
            elif result.modified_count == 0:
                return jsonify({"success": True, "message": "No changes were made"}), 200
            
            return jsonify({"success": True, "message": "max_results updated successfully"}), 200
        except Exception as e:
            print(f"Error updating max_results: {e}")
            return jsonify({"success": False, "message": "Failed to update camera"}), 500

    # Update only the image_interval of the camera in the database
    def update_camera_image_interval(self, camera_id: str, image_interval: int):
        try:
            camera_object_id = ObjectId(camera_id)
            result = self.camera_client.update_one(
                {"_id": camera_object_id},
                {"$set": {"image_interval": image_interval}}
            )

            if result.matched_count == 0:
                return jsonify({"success": False, "message": "Camera not found"}), 404
            elif result.modified_count == 0:
                return jsonify({"success": True, "message": "No changes were made"}), 200

            return jsonify({"success": True, "message": "image_interval updated successfully"}), 200
        except Exception as e:
            print(f"Error updating image_interval: {e}")
            return jsonify({"success": False, "message": "Failed to update camera"}), 500

    # Inserta una nueva camara en un parking spot en la base de datos.
    def delete_camera(self, camera_id: str):
        try:
            camera_object_id = ObjectId(camera_id)
            self.camera_client.delete_one({"_id": camera_object_id})
            return jsonify({"success": True, "message": "Camera deleted successfully"}), 201
        except Exception as e:
            print(f"Error al eliminar la cámara: {e}")
            return jsonify({"success": False, "message": "Failed to delete camera"}), 500
