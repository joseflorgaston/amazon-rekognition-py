from app.data.services.model_service import ModelService

class ModelRepository:
    def __init__(self, model_service=None):
        self.model_service = model_service or ModelService()

    def detect_labels(self, image_bytes):
        return self.model_service.detect_labels(image_bytes)

    def start_model(self):
        return self.model_service.start_model()

    def stop_model(self):
        return self.model_service.stop_model()
    
    def is_model_running(self):
        return self.model_service.is_model_running()
