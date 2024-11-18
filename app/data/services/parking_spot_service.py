from bson import ObjectId
from flask import jsonify
from app.config.mongo_client import get_mongo_client
from app.core.models.parking_spot_data import ParkingSpotData
from app.interfaces.parking_spot_interface import ParkingSpotInterface

class ParkingSpotService(ParkingSpotInterface):
    def __init__(self):
        self.db_client = get_mongo_client()
        self.parking_spot_client = self.db_client["parking-lot"]["parking_spot"]

    # Retorna las camaras guardadas en la base de datos.
    def get_parking_spots(self):
        try:
            result = self.parking_spot_client.find()
            parking_spots = list(result)

            for parking_spot in parking_spots:
                print(parking_spot)
                parking_spot["_id"] = str(parking_spot["_id"])

            return jsonify({"data": parking_spots, "success": True, "message": "parking_spot retrieved successfully"}), 200
        except Exception as e:
            print(f"Error retrieving parking spots: {e}")
            return jsonify({"success": False, "message": "Failed to retrieve parking spots"}), 500
        
    def get_parking_spot(self, parking_spot_id: str):
        try:
            parking_spot_object_id = ObjectId(parking_spot_id)
            result = self.parking_spot_client.find_one({"_id": parking_spot_object_id})
            
            if not result:
                return jsonify({"success": False, "message": "Parking spot not found"}), 404

            result["_id"] = str(result["_id"])

            return jsonify({"data": result, "success": True}), 200
        except Exception as e:
            print(f"Error retrieving parking spot: {e}")
            return jsonify({"success": False, "message": "Failed to retrieve parking spot"}), 500
        
    # Inserta un parking spot en la base de datos.
    def insert_parking_spot(self, parking_spot: ParkingSpotData):
        try:
            parking_spot = {
                "name": parking_spot.name,
                "location": parking_spot.location,
                "address": parking_spot.address,
                "created_at": parking_spot.created_at
            }
            print("inserting parking spot:")
            print(parking_spot)
            result = self.parking_spot_client.insert_one(parking_spot)
            return jsonify({"success": True, "id": str(result.inserted_id), "message": "Parking spot created successfully"}), 201
        except Exception as e:
            print(f"Error al insertar el parking spot: {e}")
            return jsonify({"success": False, "message": f"Failed to insert parking spot: {e}"}), 500
        
    # Actualiza un parking spot en la base de datos.
    def update_parking_spot(self, parking_spot_id:str, parking_spot: ParkingSpotData):
        try:
            parking_spot_object_id = ObjectId(parking_spot_id)
            parking_spot = {
                "name": parking_spot.name,
                "location": parking_spot.location,
                "address": parking_spot.address,
                "created_at": parking_spot.created_at,
            }
            
            self.parking_spot_client.find_one_and_update(
                {"_id": parking_spot_object_id},
                {"$set": parking_spot},
                return_document=True
            )
            
            return jsonify({"success": True, "message": "parking_spot updated successfully"}), 201
        except Exception as e:
            print(f'Error: {e}')
            return jsonify({"success": False, "message": "Failed to update parking_spot"}), 500

    # Elimina un parking spot en la base de datos.
    def delete_parking_spot(self, parking_spot_id: str):
        try:
            # Convertir image_id a ObjectId
            parking_spot_object_id = ObjectId(parking_spot_id)
            self.parking_spot_client.delete_one({"_id": parking_spot_object_id})
            return jsonify({"success": True, "message": "Parking spot deleted successfully"}), 201
        except Exception as e:
            return jsonify({"success": False, "message": f"Failed to delete parking spot: {e}"}), 500
