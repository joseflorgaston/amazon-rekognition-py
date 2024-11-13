import unittest
from unittest.mock import MagicMock, patch
from app.core.use_cases.start_model_use_case import StartModelUseCase
from app.core.exceptions import ModelAlreadyRunningException
from app.data.repositories.label_repository import ParkingLotRepository

class TestStartModelUseCase(unittest.TestCase):
    def setUp(self):
        self.use_case = StartModelUseCase()
        self.use_case.label_repository = MagicMock()

    def test_start_model_success(self):
        # Configura el repositorio para simular que el modelo está detenido
        self.use_case.label_repository.is_model_running.return_value = False
        self.use_case.label_repository.start_model.return_value = {"status": "starting"}

        result = self.use_case.execute()
        self.assertEqual(result["status"], "starting")

    def test_start_model_already_running(self):
        # Simula que el modelo ya está en ejecución
        self.use_case.label_repository.is_model_running.return_value = True

        with self.assertRaises(ModelAlreadyRunningException):
            self.use_case.execute()

if __name__ == '__main__':
    unittest.main()
