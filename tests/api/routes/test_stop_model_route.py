import unittest
from unittest.mock import patch
from app.main import app
from app.core.exceptions import ModelAlreadyStoppedException

class TestStopModelRoute(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('app.core.use_cases.stop_model_use_case.StopModelUseCase.execute')
    def test_stop_model_success(self, mock_execute):
        # Simula una detención exitosa
        mock_execute.return_value = {"status": "stopping"}

        response = self.client.post('/stop-model')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Model stopped successfully"})

    @patch('app.core.use_cases.stop_model_use_case.StopModelUseCase.execute')
    def test_stop_model_already_stopped(self, mock_execute):
        # Simula que el modelo ya está detenido
        mock_execute.side_effect = ModelAlreadyStoppedException("Model is already stopped")

        response = self.client.post('/stop-model')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Model is already stopped"})

if __name__ == '__main__':
    unittest.main()
