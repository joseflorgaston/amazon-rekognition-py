
from datetime import datetime
from app.core.models.camera_data import CameraData
from app.core.use_cases.camera_use_cases.insert_camera_use_case import InsertCameraUseCase
from app.core.use_cases.parking_spot_use_cases.delete_parking_spot_use_case import DeleteParkingSpotUseCase

class ParkingSpotController:
    @staticmethod
    def insert_parking_spot(data):
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
    def delete_parking_spot(parking_spot_id):
        return DeleteParkingSpotUseCase().execute(
            parking_spot_id
        )