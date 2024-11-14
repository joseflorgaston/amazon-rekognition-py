
from datetime import datetime
from app.core.models.camera_data import CameraData
from app.core.use_cases.camera_use_cases.delete_camera_use_case import DeleteCameraUseCase
from app.core.use_cases.camera_use_cases.insert_camera_use_case import InsertCameraUseCase

class CameraController:
    @staticmethod
    def insert_camera(data):
        return InsertCameraUseCase().execute(
            CameraData(
                parking_spot_id=data['parking_spot_id'],
                image_interval=data["image_interval"],
                created_at=datetime.now(),
                identifier=data['identifier'],
                max_results=data['max_results'],
            )
        )
    
    @staticmethod
    def delete_camera(camera_id):
        return DeleteCameraUseCase().execute(camera_id)