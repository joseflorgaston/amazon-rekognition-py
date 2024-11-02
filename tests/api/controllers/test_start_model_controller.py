import unittest
from unittest.mock import patch, MagicMock
from app.main import app
from app.core.exceptions import ModelAlreadyRunningException

class TestStartModelController(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('app.api.controllers.start_model_controller.StartModelUseCase')
    def test_start_model_success(self, MockStartModelUseCase):
        mock_use_case = MockStartModelUseCase.return_value
        mock_use_case.execute.return_value = {"status": "starting"}

        response = self.client.post('/start-model')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Model started successfully"})

    @patch('app.api.controllers.start_model_controller.StartModelUseCase')
    def test_start_model_already_running(self, MockStartModelUseCase):
        mock_use_case = MockStartModelUseCase.return_value
        mock_use_case.execute.side_effect = ModelAlreadyRunningException("Model is already running")

        response = self.client.post('/start-model')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Model is already running"})

if __name__ == '__main__':
    unittest.main()
