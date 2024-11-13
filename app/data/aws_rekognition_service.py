import boto3
import base64

from flask import jsonify
from PIL import ImageDraw
from app.config.mongo_client import get_mongo_client
from app.config.s3_client import get_s3_client
from app.core.models.camera_data import CameraData
from app.core.models.draw_label_data import DrawLabelData
from app.core.models.draw_labels_data import DrawLabelsData, ImageDrawed
from app.core.models.image_data import ImageData
from app.core.models.parking_spot_data import ParkingSpotData
from app.core.models.s3_image_data import S3ImageData
from app.core.use_cases.draw_label_to_image_use_case import DrawLabelToImageUseCase
from app.interfaces.aws_rekognition_interface import RekognitionInterface
from app.config.config import Config

class AwsRekognitionService(RekognitionInterface):
    def __init__(self):
        self.aws_client = boto3.client('rekognition', region_name=Config.AWS_REGION)
        self.project_arn = Config.PROJECT_ARN
        self.model_arn = Config.MODEL_ARN
        self.min_inference_units = Config.MIN_INFERENCE_UNITS
        self.version_name = Config.VERSION_NAME
        self.s3_client = get_s3_client()
        self.db_client = get_mongo_client()

    # Envia la imagen a aws rekognition y retorna las etiquetas
    def detect_labels(self, image_bytes):
        response = self.aws_client.detect_custom_labels(
            ProjectVersionArn=self.model_arn,
            Image={'Bytes': image_bytes},
            MaxResults=10,
            MinConfidence=60
        )
        return response['CustomLabels']
    
    # Activa el modelo de aws rekognition
    def start_model(self):
        response = self.aws_client.start_project_version(
            ProjectVersionArn=self.model_arn,
            MinInferenceUnits=self.min_inference_units
        )
        return response
    
    # Apaga el modelo de aws rekognition
    def stop_model(self):
        response = self.aws_client.stop_project_version(
            ProjectVersionArn=self.model_arn
        )
        return response

    # Verifica si el modelo está encendido (RUNNING) o apagado.
    def is_model_running(self):
        try:
            # Describe el estado del modelo
            response = self.aws_client.describe_project_versions(
                ProjectArn=self.project_arn,
                VersionNames=[self.version_name]
            )
            # Obtener el estado del modelo
            model_status = response['ProjectVersionDescriptions'][0]['Status']
            return model_status == "RUNNING"
        except Exception as e:
            print(f"Error al verificar el estado del modelo: {e}")
            return False

    # Decodifica una imagen en formato base64
    def decode_base64_image(self, base64_str):
        if base64_str.startswith("data:image"):
            base64_str = base64_str.split(",")[1]
        try:
            image_data = base64.b64decode(base64_str)
            return image_data
        except Exception as e:
            return jsonify({"success": False, "error": f"Failed to decode image: {e}"}), 400

    # Sube una imagen en formato base64 al s3.
    def upload_image_to_s3(self, s3_image_data: S3ImageData):
        try:
            self.s3_client.put_object(
                Bucket=s3_image_data.bucket_name,
                Key=s3_image_data.file_name,
                Body=s3_image_data.image_data,
                ContentType='image/png'
            )
            return True
        except Exception as e:
            return jsonify({"success": False, "error": f"Failed to upload image to S3: {e}"}), 500

    # Dibuja los cuadros delimitadores a la imagen.
    def draw_label_to_image(self, draw_label_data):
        try:
            left = draw_label_data.box['Left'] * draw_label_data.image.width
            top = draw_label_data.box['Top'] * draw_label_data.image.height
            width = draw_label_data.box['Width'] * draw_label_data.image.width
            height = draw_label_data.box['Height'] * draw_label_data.image.height
            draw_label_data.draw.rectangle([left, top, left + width, top + height], outline=draw_label_data.color, width=3)
            return True
        except Exception as e:
            return jsonify({"success": False, "error": f"Failed to draw label in image: {e}"}), 500


    # Dibuja los cuadros delimitadores a la imagen.
    def draw_labels_to_image(self, draw_labels_data: DrawLabelsData):
        try:
            free_count, occupied_count = 0, 0
            draw = ImageDraw.Draw(draw_labels_data.image)
            for label in draw_labels_data.labels:
                label_name = label['Name'].lower()
                color = 'green' if label_name == 'free' else 'red' if label_name == 'occupied' else None
                if color:
                    free_count += (label_name == 'free')
                    occupied_count += (label_name == 'occupied')
                    box = label['Geometry']['BoundingBox']
                    DrawLabelToImageUseCase.execute(
                        DrawLabelData(
                            image=draw_labels_data.image, draw=draw, color=color, box=box
                        )
                    )
            return ImageDrawed(free_spaces=free_count, occupied_spaces= occupied_count, image= draw_labels_data.image)
        except Exception as e:
            return jsonify({"success": False, "error": f"Failed to draw label in image: {e}"}), 500

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
            return jsonify({"success": True, "id": str(result.inserted_id)}), 201
        except Exception as e:
            print(f"Error al insertar el parking spot: {e}")
            return jsonify({"success": False, "error": "Failed to insert parking spot"}), 500

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
            return jsonify({"success": True, "id": str(result.inserted_id)}), 201
        except Exception as e:
            print(f"Error al insertar la cámara: {e}")
            return jsonify({"success": False, "error": "Failed to insert camera"}), 500
        
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
            result = self.db_client["parking-lot"]["images"].insert_one(image)
            return jsonify({"success": True, "id": str(result.inserted_id)}), 201
        except Exception as e:
            print(f"Error al insertar la imagen: {e}")
            return jsonify({"success": False, "error": "Failed to insert image"}), 500
