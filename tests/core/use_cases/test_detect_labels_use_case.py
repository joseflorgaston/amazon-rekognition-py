import unittest
from unittest.mock import MagicMock
from app.core.use_cases.detect_labels_use_case import DetectLabelsUseCase
from app.data.repositories.label_repository import ParkingLotRepository

class TestDetectLabelsUseCase(unittest.TestCase):
    def setUp(self):
        self.label_repository = ParkingLotRepository()
        self.use_case = DetectLabelsUseCase()
        self.use_case.label_repository = MagicMock()

    def test_detect_labels_success(self):
        # Configura la respuesta simulada del repositorio
        self.use_case.label_repository.detect_labels.return_value = [
            {'Name': 'Car', 'Confidence': 95.7},
            {'Name': 'ParkingSpot', 'Confidence': 87.2}
        ]

        # Ejecuta el caso de uso
        image_bytes = b'sample_image_data'
        result = self.use_case.execute(image_bytes)

        # Verifica el resultado
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['Name'], 'Car')
        self.assertEqual(result[1]['Name'], 'ParkingSpot')

    def test_detect_labels_no_labels(self):
        self.use_case.label_repository.detect_labels.return_value = []

        image_bytes = b'sample_image_data'
        result = self.use_case.execute(image_bytes)

        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
