import unittest
from unittest.mock import patch, MagicMock
from app.main import app

class TestCheckModelStatusController(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('app.api.controllers.check_model_status_controller.CheckModelStatusUseCase')
    def test_check_model_status_running(self, MockCheckModelStatusUseCase):
        mock_use_case = MockCheckModelStatusUseCase.return_value
        mock_use_case.execute.return_value = True

        response = self.client.get('/model-status')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "Running"})

    @patch('app.api.controllers.check_model_status_controller.CheckModelStatusUseCase')
    def test_check_model_status_stopped(self, MockCheckModelStatusUseCase):
        mock_use_case = MockCheckModelStatusUseCase.return_value
        mock_use_case.execute.return_value = False

        response = self.client.get('/model-status')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "Stopped"})

if __name__ == '__main__':
    unittest.main()
