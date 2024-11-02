import unittest
from unittest.mock import MagicMock, patch
from app.core.use_cases.stop_model_use_case import StopModelUseCase
from app.core.exceptions import ModelAlreadyStoppedException
from app.data.repositories.label_repository import LabelRepository

class TestStopModelUseCase(unittest.TestCase):
    def setUp(self):
        self.use_case = StopModelUseCase()
        self.use_case.label_repository = MagicMock()

    def test_stop_model_success(self):
        # Configura el repositorio para simular que el modelo está en ejecución
        self.use_case.label_repository.is_model_running.return_value = True
        self.use_case.label_repository.stop_model.return_value = {"status": "stopping"}

        result = self.use_case.execute()
        self.assertEqual(result["status"], "stopping")

    def test_stop_model_already_stopped(self):
        # Simula que el modelo ya está detenido
        self.use_case.label_repository.is_model_running.return_value = False

        with self.assertRaises(ModelAlreadyStoppedException):
            self.use_case.execute()

if __name__ == '__main__':
    unittest.main()
