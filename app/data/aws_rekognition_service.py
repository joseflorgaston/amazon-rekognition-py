import boto3
import os
from app.interfaces.aws_rekognition_interface import RekognitionInterface

class AwsRekognitionService(RekognitionInterface):
    def __init__(self):
        self.client = boto3.client('rekognition', region_name=os.getenv('AWS_REGION'))
        self.project_arn = os.getenv('PROJECT_ARN')
        self.model_arn = os.getenv('MODEL_ARN')
        self.min_inference_units = int(os.getenv('MIN_INFERENCE_UNITS', 1))

    def detect_labels(self, image_bytes):
        response = self.client.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=10,
            MinConfidence=80
        )
        return response['Labels']
    
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
                VersionNames=[os.getenv('VERSION_NAME')]
            )
            # Obtener el estado del modelo
            model_status = response['ProjectVersionDescriptions'][0]['Status']
            return model_status == "RUNNING"
        except Exception as e:
            print(f"Error al verificar el estado del modelo: {e}")
            return False
