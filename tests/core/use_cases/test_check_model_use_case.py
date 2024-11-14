import unittest
from unittest.mock import MagicMock
from app.core.use_cases.model_use_cases.check_model_status_use_case import CheckModelStatusUseCase
from app.data.repositories.label_repository import ParkingLotRepository

class TestCheckModelStatusUseCase(unittest.TestCase):
    def setUp(self):
        self.use_case = CheckModelStatusUseCase()
        self.use_case.label_repository = MagicMock()

    def test_check_model_status_running(self):
        # Simula que el modelo está en ejecución
        self.use_case.label_repository.is_model_running.return_value = True
        status = self.use_case.execute()
        self.assertTrue(status)

    def test_check_model_status_stopped(self):
        # Simula que el modelo está detenido
        self.use_case.label_repository.is_model_running.return_value = False
        status = self.use_case.execute()
        self.assertFalse(status)

if __name__ == '__main__':
    unittest.main()
