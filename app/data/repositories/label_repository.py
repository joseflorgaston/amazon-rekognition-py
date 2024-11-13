from app.core.models.camera_data import CameraData
from app.core.models.draw_label_data import DrawLabelData
from app.core.models.draw_labels_data import DrawLabelsData
from app.core.models.image_data import ImageData
from app.core.models.parking_spot_data import ParkingSpotData
from app.core.models.s3_image_data import S3ImageData
from app.data.aws_rekognition_service import AwsRekognitionService

class ParkingLotRepository:
    def __init__(self, rekognition_service=None):
        self.rekognition_service = rekognition_service or AwsRekognitionService()

    def detect_labels(self, image_bytes):
        return self.rekognition_service.detect_labels(image_bytes)

    def start_model(self):
        return self.rekognition_service.start_model()

    def stop_model(self):
        return self.rekognition_service.stop_model()
    
    def is_model_running(self):
        return self.rekognition_service.is_model_running()
    
    def decode_base64_image(self, base64_str):
        return self.rekognition_service.decode_base64_image(base64_str)

    def upload_image_to_s3(self, s3_image_data: S3ImageData):
        return self.rekognition_service.upload_image_to_s3(s3_image_data)
    
    def draw_label_to_image(self, draw_label_data: DrawLabelData):
        return self.rekognition_service.draw_label_to_image(draw_label_data)
    
    def draw_labels_to_image(self, draw_labels_data: DrawLabelsData):
        return self.rekognition_service.draw_labels_to_image(draw_labels_data)
    
    def insert_parking_spot(self, parking_spot: ParkingSpotData):
        return self.rekognition_service.insert_parking_spot(parking_spot)
    
    def insert_camera(self, camera: CameraData):
        return self.rekognition_service.insert_camera(camera)
    
    def insert_image(self, image: ImageData):
        return self.rekognition_service.insert_image(image)
