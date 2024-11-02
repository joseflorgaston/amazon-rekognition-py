import unittest
from unittest.mock import patch, MagicMock
from app.main import app

class TestDetectLabelsController(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.image_data = (b'--boundary\r\n'
                           b'Content-Disposition: form-data; name="image"; filename="test.jpg"\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n'
                           b'testimagecontent\r\n'
                           b'--boundary--\r\n')
        self.headers = {'Content-Type': 'multipart/form-data; boundary=boundary'}

    @patch('app.api.controllers.detect_labels_controller.DetectLabelsUseCase')
    def test_detect_labels_success(self, MockDetectLabelsUseCase):
        # Mock del caso de uso
        mock_use_case = MockDetectLabelsUseCase.return_value
        mock_use_case.execute.return_value = [{'Name': 'Car', 'Confidence': 95.7}]

        # Llamada al endpoint
        response = self.client.post('/detect-labels', data=self.image_data, headers=self.headers)

        # Verificar respuesta
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'labels': [{'Name': 'Car', 'Confidence': 95.7}]})

    @patch('app.api.controllers.detect_labels_controller.DetectLabelsUseCase')
    def test_detect_labels_no_image_provided(self, MockDetectLabelsUseCase):
        response = self.client.post('/detect-labels')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'No image file provided'})

if __name__ == '__main__':
    unittest.main()
