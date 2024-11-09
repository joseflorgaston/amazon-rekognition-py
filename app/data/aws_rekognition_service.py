import boto3
from app.interfaces.aws_rekognition_interface import RekognitionInterface
from app.config.config import Config

class AwsRekognitionService(RekognitionInterface):
    def __init__(self):
        self.client = boto3.client('rekognition', region_name=Config.AWS_REGION)
        self.project_arn = Config.PROJECT_ARN
        self.model_arn = Config.MODEL_ARN
        self.min_inference_units = Config.MIN_INFERENCE_UNITS
        self.version_name = Config.VERSION_NAME

    def detect_labels(self, image_bytes):
        response = self.client.detect_custom_labels(
            ProjectVersionArn=self.model_arn,
            Image={'Bytes': image_bytes},
            MaxResults=10,
            MinConfidence=60
        )
        return response['CustomLabels']
    
    def start_model(self):
        response = self.client.start_project_version(
            ProjectVersionArn=self.model_arn,
            MinInferenceUnits=self.min_inference_units
        )
        return response
    
    def stop_model(self):
        response = self.client.stop_project_version(
            ProjectVersionArn=self.model_arn
        )
        return response

    def is_model_running(self):
        """
        Verifica si el modelo está encendido (RUNNING) o apagado.
        """
        try:
            # Describe el estado del modelo
            response = self.client.describe_project_versions(
                ProjectArn=self.project_arn,
                VersionNames=[self.version_name]
            )
            # Obtener el estado del modelo
            model_status = response['ProjectVersionDescriptions'][0]['Status']
            return model_status == "RUNNING"
        except Exception as e:
            print(f"Error al verificar el estado del modelo: {e}")
            return False
