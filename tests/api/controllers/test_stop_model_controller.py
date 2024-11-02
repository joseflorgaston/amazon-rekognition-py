import unittest
from unittest.mock import patch, MagicMock
from app.main import app
from app.core.exceptions import ModelAlreadyStoppedException

class TestStopModelController(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('app.api.controllers.stop_model_controller.StopModelUseCase')
    def test_stop_model_success(self, MockStopModelUseCase):
        mock_use_case = MockStopModelUseCase.return_value
        mock_use_case.execute.return_value = {"status": "stopping"}

        response = self.client.post('/stop-model')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Model stopped successfully"})

    @patch('app.api.controllers.stop_model_controller.StopModelUseCase')
    def test_stop_model_already_stopped(self, MockStopModelUseCase):
        mock_use_case = MockStopModelUseCase.return_value
        mock_use_case.execute.side_effect = ModelAlreadyStoppedException("Model is already stopped")

        response = self.client.post('/stop-model')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Model is already stopped"})

if __name__ == '__main__':
    unittest.main()
