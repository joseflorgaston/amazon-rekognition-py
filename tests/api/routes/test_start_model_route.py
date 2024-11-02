import unittest
from unittest.mock import patch
from app.main import app
from app.core.exceptions import ModelAlreadyRunningException

class TestStartModelRoute(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('app.core.use_cases.start_model_use_case.StartModelUseCase.execute')
    def test_start_model_success(self, mock_execute):
        # Simula un inicio exitoso
        mock_execute.return_value = {"status": "starting"}

        response = self.client.post('/start-model')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Model started successfully"})

    @patch('app.core.use_cases.start_model_use_case.StartModelUseCase.execute')
    def test_start_model_already_running(self, mock_execute):
        # Simula que el modelo ya está en ejecución
        mock_execute.side_effect = ModelAlreadyRunningException("Model is already running")

        response = self.client.post('/start-model')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Model is already running"})

if __name__ == '__main__':
    unittest.main()
