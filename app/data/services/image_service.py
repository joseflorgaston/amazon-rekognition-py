from bson import ObjectId
from flask import jsonify
from app.config.mongo_client import get_mongo_client
from app.core.models.image_data import ImageData
from app.interfaces.image_interface import ImageInterface

class ImageService(ImageInterface):
    def __init__(self):
        self.db_client = get_mongo_client()
        self.image_client = self.db_client["parking-lot"]["images"]

    # Retorna la ultima imagen guardada en la base de datos de una camara especifica:
    def get_last_image(self, camera_id: str):
        try:
            camera_object_id = ObjectId(camera_id)

            last_image = self.image_client.find_one(
                {"camera_id": camera_object_id},
                sort=[("created_at", -1)]
            )

            # Check if an image was found
            if last_image:
                last_image["_id"] = str(last_image["_id"])
                last_image["camera_id"] = str(last_image["camera_id"])
                last_image["parking_spot_id"] = str(last_image["parking_spot_id"])
                return jsonify({"data": last_image, "success": True, "message": "Last image retrieved successfully"}), 200
            else:
                return jsonify({"success": False, "message": "No images found for the given camera"}), 404

        except Exception as e:
            print(f"Error retrieving last image: {e}")
            return jsonify({"success": False, "error": "Failed to get image"}), 500

    # Inserta una nueva imagen de una camara especifica en la base de datos.
    def insert_image(self, image: ImageData):
        try:
            image = {
                "parking_spot_id": image.parking_spot_id,
                "camera_id": image.camera_id,
                "labeled_image_url": image.labeled_image_url,
                "original_image_url": image.original_image_url,
                "free_spaces": image.free_spaces,
                "occupied_spaces": image.occupied_spaces,
                "date": image.date
            }
            result = self.image_client.insert_one(image)
            return jsonify({"success": True, "id": str(result.inserted_id), "message": "Camera created successfully"}), 201
        except Exception as e:
            print(f"Error al insertar la imagen: {e}")
            return jsonify({"success": False, "error": "Failed to insert image"}), 500

    # Elimina una imagen en la base de datos.
    def delete_image(self, image_id: str):
        try:
            # Convertir image_id a ObjectId
            image_object_id = ObjectId(image_id)
            
            # Intentar eliminar el documento en la colección de imágenes
            result = self.image_client.delete_one({"_id": image_object_id})
            
            # Verificar si se eliminó el documento
            if result.deleted_count == 1:
                return jsonify({"success": True, "message": "Image deleted successfully"}), 200
            else:
                return jsonify({"success": False, "error": "Image not found"}), 404
        except Exception as e:
            print(f"Error al eliminar la imagen: {e}")
            return jsonify({"success": False, "error": "Failed to delete image"}), 500
