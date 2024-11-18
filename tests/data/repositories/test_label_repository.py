import unittest
from unittest.mock import patch, MagicMock
from app.data.repositories.label_repository import ParkingLotRepository

class TestLabelRepository(unittest.TestCase):
    def setUp(self):
        self.repository = ParkingLotRepository()

    @patch('app.data.repositories.label_repository.boto3.client')
    def test_detect_labels_success(self, mock_boto_client):
        # Configura el cliente simulado de Rekognition
        mock_rekognition = mock_boto_client.return_value
        mock_rekognition.detect_labels.return_value = {
            'Labels': [
                {'Name': 'Car', 'Confidence': 95.7},
                {'Name': 'ParkingSpot', 'Confidence': 87.2}
            ]
        }

        image_bytes = b'sample_image_data'
        labels = self.repository.detect_labels(image_bytes)

        # Verificaciones
        self.assertEqual(len(labels), 2)
        self.assertEqual(labels[0]['Name'], 'Car')
        self.assertEqual(labels[1]['Name'], 'ParkingSpot')
        mock_rekognition.detect_labels.assert_called_once()

    @patch('app.data.repositories.label_repository.boto3.client')
    def test_detect_labels_no_labels(self, mock_boto_client):
        mock_rekognition = mock_boto_client.return_value
        mock_rekognition.detect_labels.return_value = {'Labels': []}

        image_bytes = b'sample_image_data'
        labels = self.repository.detect_labels(image_bytes)

        self.assertEqual(labels, [])
        mock_rekognition.detect_labels.assert_called_once()

    @patch('app.data.repositories.label_repository.boto3.client')
    def test_start_model_success(self, mock_boto_client):
        mock_rekognition = mock_boto_client.return_value
        mock_rekognition.start_project_version.return_value = {"Status": "starting"}

        response = self.repository.start_model()
        self.assertEqual(response["Status"], "starting")
        mock_rekognition.start_project_version.assert_called_once()

    @patch('app.data.repositories.label_repository.boto3.client')
    def test_start_model_already_running(self, mock_boto_client):
        mock_rekognition = mock_boto_client.return_value
        mock_rekognition.start_project_version.side_effect = Exception("Model is already running")

        with self.assertRaises(Exception) as context:
            self.repository.start_model()
        self.assertEqual(str(context.exception), "Model is already running")
        mock_rekognition.start_project_version.assert_called_once()

    @patch('app.data.repositories.label_repository.boto3.client')
    def test_stop_model_success(self, mock_boto_client):
        mock_rekognition = mock_boto_client.return_value
        mock_rekognition.stop_project_version.return_value = {"Status": "stopping"}

        response = self.repository.stop_model()
        self.assertEqual(response["Status"], "stopping")
        mock_rekognition.stop_project_version.assert_called_once()

    @patch('app.data.repositories.label_repository.boto3.client')
    def test_stop_model_already_stopped(self, mock_boto_client):
        mock_rekognition = mock_boto_client.return_value
        mock_rekognition.stop_project_version.side_effect = Exception("Model is already stopped")

        with self.assertRaises(Exception) as context:
            self.repository.stop_model()
        self.assertEqual(str(context.exception), "Model is already stopped")
        mock_rekognition.stop_project_version.assert_called_once()

    @patch('app.data.repositories.label_repository.boto3.client')
    def test_is_model_running_true(self, mock_boto_client):
        mock_rekognition = mock_boto_client.return_value
        mock_rekognition.describe_project_versions.return_value = {
            'ProjectVersionDescriptions': [{'Status': 'RUNNING'}]
        }

        status = self.repository.is_model_running()
        self.assertTrue(status)
        mock_rekognition.describe_project_versions.assert_called_once()

    @patch('app.data.repositories.label_repository.boto3.client')
    def test_is_model_running_false(self, mock_boto_client):
        mock_rekognition = mock_boto_client.return_value
        mock_rekognition.describe_project_versions.return_value = {
            'ProjectVersionDescriptions': [{'Status': 'STOPPED'}]
        }

        status = self.repository.is_model_running()
        self.assertFalse(status)
        mock_rekognition.describe_project_versions.assert_called_once()

if __name__ == '__main__':
    unittest.main()
