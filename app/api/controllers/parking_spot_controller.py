
from datetime import datetime
from app.core.models.parking_spot_data import ParkingSpotData
from app.core.use_cases.camera_use_cases.insert_camera_use_case import InsertCameraUseCase
from app.core.use_cases.parking_spot_use_cases.delete_parking_spot_use_case import DeleteParkingSpotUseCase
from app.core.use_cases.parking_spot_use_cases.get_parking_spot_use_case import GetParkingSpotUseCase
from app.core.use_cases.parking_spot_use_cases.get_parking_spots_use_case import GetParkingSpotsUseCase
from app.core.use_cases.parking_spot_use_cases.insert_parking_spot_use_case import InsertParkingSpotUseCase
from app.core.use_cases.parking_spot_use_cases.update_parking_spot_use_case import UpdateParkingSpotUseCase

class ParkingSpotController:
    @staticmethod
    def get_parking_spots():
        return GetParkingSpotsUseCase().execute()
    
    @staticmethod
    def get_parking_spot(parking_spot_id: str):
        return GetParkingSpotUseCase().execute(parking_spot_id=parking_spot_id)
    
    @staticmethod
    def insert_parking_spot(data):
        return InsertParkingSpotUseCase().execute(
            ParkingSpotData(
                name= data['name'],
                location= data["location"],
                address= data['address'],
                created_at= datetime.now(),
            )
        )
    
    @staticmethod
    def update_parking_spot(parking_spot_id: str, data):
        return UpdateParkingSpotUseCase().execute(
            parking_spot_id,
            ParkingSpotData(
                name= data['name'],
                location= data["location"],
                address= data['address'],
                created_at= data['created_at'],
            )
        )
        
    @staticmethod
    def delete_parking_spot(parking_spot_id):
        return DeleteParkingSpotUseCase().execute(
            parking_spot_id
        )