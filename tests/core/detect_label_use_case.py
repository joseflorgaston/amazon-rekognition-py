import unittest
from unittest.mock import MagicMock
from app.core.use_cases.detect_label_use_case import DetectLabelsUseCase
from app.data.repositories.label_repository import LabelRepository

class DetectLabelsUseCaseTest(unittest.TestCase):
    def test_detect_labels(self):
        # Configurar un mock para el repositorio
        mock_repo = MagicMock(LabelRepository)
        mock_repo.detect_labels.return_value = [
            {"Name": "Car", "Confidence": 98.5},
            {"Name": "Person", "Confidence": 95.2}
        ]

        # Crear el caso de uso con el repositorio mockeado
        use_case = DetectLabelsUseCase(label_repository=mock_repo)
        result = use_case.execute(b'test_image_bytes')

        # Verificar que el resultado es el esperado
        expected_result = [
            {"Name": "Car", "Confidence": 98.5},
            {"Name": "Person", "Confidence": 95.2}
        ]
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
