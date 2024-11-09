from flask import jsonify
from app.config.logging_config import logger
from app.core.use_cases.start_model_use_case import StartModelUseCase
from app.core.use_cases.stop_model_use_case import StopModelUseCase
from app.core.use_cases.check_model_status_use_case import CheckModelStatusUseCase
from app.core.exceptions import ModelAlreadyRunningException, ModelAlreadyStoppedException

class ModelController:
    @staticmethod
    def start_model():
        try:
            logger.info("Starting the model")
            StartModelUseCase().execute()
            logger.info("Model started successfully")
            return jsonify({"success": True, "message": "Model started successfully"}), 200
        except ModelAlreadyRunningException:
            logger.warning("Model is already running.")
            return jsonify({"success": False, "error": "Model is already running"}), 400

    @staticmethod
    def stop_model():
        try:
            logger.info("Stopping the model")
            StopModelUseCase().execute()
            logger.info("Model stopped successfully")
            return jsonify({"success": True, "message": "Model stopped successfully"}), 200
        except ModelAlreadyStoppedException:
            logger.warning("Model is already stopped.")
            return jsonify({"success": False, "message": "Model is already stopped"}), 400

    @staticmethod
    def model_status():
        try:
            logger.info("Checking model status")
            status = CheckModelStatusUseCase().execute()
            logger.info(f"Model status: {'Running' if status else 'Stopped'}")
            return jsonify({"is_running": status, "status": "Running" if status else "Stopped"}), 200
        except Exception as e:
            logger.error("Error in /model-status endpoint", exc_info=True)
            return jsonify({"error": "Failed to retrieve model status"}), 500
