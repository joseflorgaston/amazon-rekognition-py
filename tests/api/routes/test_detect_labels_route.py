import unittest
from unittest.mock import patch
from app.main import app

class TestDetectLabelsRoute(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.image_data = (b'--boundary\r\n'
                           b'Content-Disposition: form-data; name="image"; filename="test.jpg"\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n'
                           b'testimagecontent\r\n'
                           b'--boundary--\r\n')
        self.headers = {'Content-Type': 'multipart/form-data; boundary=boundary'}

    @patch('app.core.use_cases.detect_labels_use_case.DetectLabelsUseCase.execute')
    def test_detect_labels_success(self, mock_execute):
        # Simula el retorno del caso de uso
        mock_execute.return_value = [{'Name': 'Car', 'Confidence': 95.7}]

        response = self.client.post('/detect-labels', data=self.image_data, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'labels': [{'Name': 'Car', 'Confidence': 95.7}]})

    def test_detect_labels_no_image_provided(self):
        response = self.client.post('/detect-labels')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'No image file provided'})

if __name__ == '__main__':
    unittest.main()
