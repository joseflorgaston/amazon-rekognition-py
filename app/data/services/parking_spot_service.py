from bson import ObjectId
from flask import jsonify
from app.config.mongo_client import get_mongo_client
from app.core.models.parking_spot_data import ParkingSpotData
from app.interfaces.aws_rekognition_interface import RekognitionInterface

class ParkingSpotService(RekognitionInterface):
    def __init__(self):
        self.db_client = get_mongo_client()

    # Inserta un parking spot en la base de datos.
    def insert_parking_spot(self, parking_spot: ParkingSpotData):
        try:
            parking_spot = {
                "name": parking_spot.name,
                "location": parking_spot.location,
                "address": parking_spot.address,
                "createdAt": parking_spot.created_at
            }
            result = self.db_client["parking-lot"]["parking_spot"].insert_one(parking_spot)
            return jsonify({"success": True, "id": str(result.inserted_id), "message": "Parking spot created successfully"}), 201
        except Exception as e:
            print(f"Error al insertar el parking spot: {e}")
            return jsonify({"success": False, "message": f"Failed to insert parking spot: {e}"}), 500

    # Inserta un parking spot en la base de datos.
    def delete_parking_spot(self, parking_spot_id: str):
        try:
            # Convertir image_id a ObjectId
            parking_spot_object_id = ObjectId(parking_spot_id)
            self.db_client["parking-lot"]["parking_spot"].delete_one(parking_spot_object_id)
            return jsonify({"success": True, "message": "Parking spot deleted successfully"}), 201
        except Exception as e:
            return jsonify({"success": False, "message": f"Failed to insert parking spot: {e}"}), 500
