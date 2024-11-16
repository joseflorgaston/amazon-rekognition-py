from abc import ABC, abstractmethod

class ModelInterface(ABC):
    @abstractmethod
    def detect_labels(self, image_bytes):
        pass
    
    @abstractmethod
    def start_model(self):
        pass

    @abstractmethod
    def stop_model(self):
        pass

    @abstractmethod
    def is_model_running(self):
        pass
