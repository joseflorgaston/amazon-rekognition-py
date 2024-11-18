from datetime import datetime
from app.core.models.camera_data import CameraData
from app.core.use_cases.camera_use_cases.delete_camera_use_case import DeleteCameraUseCase
from app.core.use_cases.camera_use_cases.get_cameras_use_case import GetCamerasUseCase
from app.core.use_cases.camera_use_cases.get_parking_spot_cameras_use_case import GetParkingSpotCamerasUseCase
from app.core.use_cases.camera_use_cases.insert_camera_use_case import InsertCameraUseCase
from app.core.use_cases.camera_use_cases.update_camera_max_results_use_case import UpdateCameraMaxResultsUseCase
from app.core.use_cases.camera_use_cases.update_camera_image_interval_use_case import UpdateCameraImageIntervalUseCase
from app.core.use_cases.camera_use_cases.update_camera_use_case import UpdateCameraUseCase

class CameraController:
    @staticmethod
    def get_cameras():
        return GetCamerasUseCase().execute()

    @staticmethod
    def get_parking_spot_cameras(parking_spot_id: str):
        return GetParkingSpotCamerasUseCase().execute(parking_spot_id)

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
    def update_camera(camera_id: str, data):
        return UpdateCameraUseCase().execute(
            camera_id,
            CameraData(
                parking_spot_id=data['parking_spot_id'],
                image_interval=data["image_interval"],
                created_at=datetime.now(),
                identifier=data['identifier'],
                max_results=data['max_results'],
            )
        )

    @staticmethod
    def update_camera_max_results(camera_id: str, data):
        return UpdateCameraMaxResultsUseCase().execute(
            camera_id, data['max_results']
        )

    @staticmethod
    def update_camera_image_interval(camera_id: str, data):
        return UpdateCameraImageIntervalUseCase().execute(
            camera_id, data['image_interval']
        )

    @staticmethod
    def delete_camera(camera_id: str):
        print(camera_id)
        return DeleteCameraUseCase().execute(camera_id)
