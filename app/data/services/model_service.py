import boto3
from app.config.config import Config
from app.interfaces.aws_rekognition_interface import RekognitionInterface

class ModelService(RekognitionInterface):
    def __init__(self):
        self.aws_client = boto3.client('rekognition', region_name=Config.AWS_REGION)

    # Envia la imagen a aws rekognition y retorna las etiquetas
    def detect_labels(self, image_bytes):
        response = self.aws_client.detect_custom_labels(
            ProjectVersionArn=self.model_arn,
            Image={'Bytes': image_bytes},
            MaxResults=10,
            MinConfidence=60
        )
        return response['CustomLabels']
    
    # Activa el modelo de aws rekognition
    def start_model(self):
        response = self.aws_client.start_project_version(
            ProjectVersionArn=self.model_arn,
            MinInferenceUnits=self.min_inference_units
        )
        return response
    
    # Apaga el modelo de aws rekognition
    def stop_model(self):
        response = self.aws_client.stop_project_version(
            ProjectVersionArn=self.model_arn
        )
        return response

    # Verifica si el modelo está encendido (RUNNING) o apagado.
    def is_model_running(self):
        try:
            # Describe el estado del modelo
            response = self.aws_client.describe_project_versions(
                ProjectArn=self.project_arn,
                VersionNames=[self.version_name]
            )
            # Obtener el estado del modelo
            model_status = response['ProjectVersionDescriptions'][0]['Status']
            return model_status == "RUNNING"
        except Exception as e:
            return False
