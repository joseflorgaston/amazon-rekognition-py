import unittest
from unittest.mock import patch
from app.main import app

class TestModelStatusRoute(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('app.core.use_cases.check_model_status_use_case.CheckModelStatusUseCase.execute')
    def test_model_status_running(self, mock_execute):
        # Simula que el modelo está en ejecución
        mock_execute.return_value = True

        response = self.client.get('/model-status')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "Running"})

    @patch('app.core.use_cases.check_model_status_use_case.CheckModelStatusUseCase.execute')
    def test_model_status_stopped(self, mock_execute):
        # Simula que el modelo está detenido
        mock_execute.return_value = False

        response = self.client.get('/model-status')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "Stopped"})

if __name__ == '__main__':
    unittest.main()
