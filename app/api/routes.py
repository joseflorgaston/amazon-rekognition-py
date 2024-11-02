from flask import Blueprint, jsonify, request
from app.config.logging_config import logger
from app.core.use_cases.detect_label_use_case import DetectLabelsUseCase
from app.core.use_cases.start_model_use_case import StartModelUseCase
from app.core.use_cases.stop_model_use_case import StopModelUseCase
from app.core.use_cases.check_model_status_use_case import CheckModelStatusUseCase
from app.core.exceptions import ModelAlreadyRunningException, ModelAlreadyStoppedException

routes = Blueprint('routes', __name__)

@routes.route('/detect-labels', methods=['POST'])
def detect_labels():
    try:
        if 'image' not in request.files:
            logger.warning("No image found in the request.")
            return jsonify({"error": "No image file provided"}), 400
        
        image = request.files['image'].read()
        logger.info("Received image for label detection")

        # Call the use case to detect labels
        labels = DetectLabelsUseCase().execute(image)
        logger.info(f"Labels detected: {labels}")
        
        return jsonify({"labels": labels}), 200
    except Exception as e:
        logger.error("Error in /detect-labels endpoint", exc_info=True)
        return jsonify({"error": "Failed to detect labels"}), 500


@routes.route('/start-model', methods=['POST'])
def start_model():
    try:
        logger.info("Starting the model")
        StartModelUseCase().execute()
        logger.info("Model started successfully")
        return jsonify({"message": "Model started successfully"}), 200
    except ModelAlreadyRunningException as e:
        logger.warning("Model is already running.")
        return jsonify({"error": "Model is already running"}), 400
    except Exception as e:
        logger.error("Error in /start-model endpoint", exc_info=True)
        return jsonify({"error": "Failed to start the model"}), 500


@routes.route('/stop-model', methods=['POST'])
def stop_model():
    try:
        logger.info("Stopping the model")
        StopModelUseCase().execute()
        logger.info("Model stopped successfully")
        return jsonify({"message": "Model stopped successfully"}), 200
    except ModelAlreadyStoppedException as e:
        logger.warning("Model is already stopped.")
        return jsonify({"error": "Model is already stopped"}), 400
    except Exception as e:
        logger.error("Error in /stop-model endpoint", exc_info=True)
        return jsonify({"error": "Failed to stop the model"}), 500


@routes.route('/model-status', methods=['GET'])
def model_status():
    try:
        logger.info("Checking model status")
        status = CheckModelStatusUseCase().execute()
        logger.info(f"Model status: {'Running' if status else 'Stopped'}")
        return jsonify({"status": "Running" if status else "Stopped"}), 200
    except Exception as e:
        logger.error("Error in /model-status endpoint", exc_info=True)
        return jsonify({"error": "Failed to retrieve model status"}), 500
