from abc import ABC, abstractmethod

class RekognitionInterface(ABC):
    @abstractmethod
    def detect_labels(self, image_bytes):
        pass
