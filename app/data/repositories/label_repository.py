from app.data.aws_rekognition_service import AwsRekognitionService

class LabelRepository:
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
