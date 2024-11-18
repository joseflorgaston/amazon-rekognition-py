import boto3
from flask import jsonify
from app.config.config import Config
from app.core.exceptions import ModelAlreadyStoppedException
from app.interfaces.model_interface import ModelInterface
from app.config.logging_config import logger

class ModelService(ModelInterface):
    def __init__(self):
        self.aws_client = boto3.client('rekognition', region_name=Config.AWS_REGION)
        self.model_arn = Config.MODEL_ARN
        self.min_inference_units = Config.MIN_INFERENCE_UNITS
        self.project_arn = Config.PROJECT_ARN
        self.version_name = Config.VERSION_NAME

    # Deprecated("use insert image instead")
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
        try:
            logger.info("Starting the model")
            self.aws_client.start_project_version(
                ProjectVersionArn=self.model_arn,
                MinInferenceUnits=self.min_inference_units
            )
            logger.info("Model started successfully")
            return jsonify({"success": True, "message": f"Model started successfully"}), 200
        except Exception as e:
            logger.warning("Failed to start model: {e}")
            return jsonify({"success": False, "error": f"Failed to start model: {e}"}), 500
    
    # Apaga el modelo de aws rekognition
    def stop_model(self):
        try:
            logger.info("Stopping the model")
            self.aws_client.stop_project_version(
                ProjectVersionArn=self.model_arn
            )
            logger.info("Model stopped successfully")
            return jsonify({"success": True, "message": f"Model stopped successfully"}), 200
        except ModelAlreadyStoppedException:
            logger.error("Model already stopped", exc_info=True)
            return jsonify({"success": False, "message": "Model is already stopped"}), 400
        except Exception as e:
            logger.warning("Error in /model/stop endpoint")
            return jsonify({"success": False, "error": f"Failed to stop model: {e}"}), 500

    # Verifica si el modelo está encendido (RUNNING) o apagado.
    def is_model_running(self):
        try:
            response = self.aws_client.describe_project_versions(
                ProjectArn=self.project_arn,
                VersionNames=[self.version_name]
            )
            model_status = response['ProjectVersionDescriptions'][0]['Status']
            logger.info(f"Model status: {model_status}")
            return jsonify({"success": True, "status": model_status}), 200
        except Exception as e:
            logger.error("Error in /model/status endpoint", exc_info=True)
            return jsonify({"success": False, "error": f"Failed to check model status: {e}"}), 500
