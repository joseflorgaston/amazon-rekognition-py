import base64
import io
from flask import Blueprint, jsonify, request
from PIL import Image, ImageDraw, UnidentifiedImageError
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
        data = request.get_json()
        if 'image' not in data:
            return jsonify({"success": False, "error": "No image data provided"}), 400

        # Limpiar el prefijo si está presente y decodificar la imagen en base64
        base64_str = data['image']
        if base64_str.startswith("data:image"):
            base64_str = base64_str.split(",")[1]
        image_data = base64.b64decode(base64_str)

        # Intentar abrir la imagen usando PIL
        try:
            image = Image.open(io.BytesIO(image_data))
        except UnidentifiedImageError as e:
            print(e)
            return jsonify({"success": False, "error": "Failed to process image"}), 400

        # Ejecutar el caso de uso para detectar etiquetas
        labels = DetectLabelsUseCase().execute(image_data)  # labels será una lista de CustomLabels
        # Contadores para espacios libres y ocupados
        free_count = 0
        occupied_count = 0

        # Dibujar los cuadros sobre la imagen y contar los espacios
        draw = ImageDraw.Draw(image)
        for label in labels:
            label_name = label['Name'].lower()
            if label_name == 'free':
                color = 'green'
                free_count += 1
            elif label_name == 'occupied':
                color = 'red'
                occupied_count += 1
            else:
                continue

            # Asume que `label` tiene coordenadas de "BoundingBox"
            box = label['Geometry']['BoundingBox']
            left = box['Left'] * image.width
            top = box['Top'] * image.height
            width = box['Width'] * image.width
            height = box['Height'] * image.height
            draw.rectangle([left, top, left + width, top + height], outline=color, width=3)

        # Convertir la imagen de nuevo a base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Devolver la imagen junto con los contadores de espacios libres y ocupados
        return jsonify({
            "success": True,
            "image": img_base64,
            "free_spaces": free_count,
            "occupied_spaces": occupied_count
        }), 200
    except Exception as e:
        print(f"Error en /detect-labels: {e}")
        return jsonify({"success": False, "error": "Failed to process image"}), 500


@routes.route('/start-model', methods=['POST'])
def start_model():
    try:
        logger.info("Starting the model")
        StartModelUseCase().execute()
        logger.info("Model started successfully")
        return jsonify({"success": True, "message": "Model started successfully"}), 200
    except ModelAlreadyRunningException as e:
        logger.warning("Model is already running.")
        return jsonify({"success": False, "error": "Model is already running"}), 400
    except Exception as e:
        logger.error("Error in /start-model endpoint", exc_info=True)
        return jsonify({"success": False, "error": "Failed to start the model"}), 500


@routes.route('/stop-model', methods=['POST'])
def stop_model():
    try:
        logger.info("Stopping the model")
        StopModelUseCase().execute()
        logger.info("Model stopped successfully")
        return jsonify({"success": True, "message": "Model stopped successfully"}), 200
    except ModelAlreadyStoppedException as e:
        logger.warning("Model is already stopped.")
        return jsonify({"success": False, "message": "Model is already stopped"}), 400
    except Exception as e:
        logger.error("Error in /stop-model endpoint", exc_info=True)
        return jsonify({"success": False, "message": "Failed to stop the model"}), 500


@routes.route('/model-status', methods=['GET'])
def model_status():
    try:
        logger.info("Checking model status")
        status = CheckModelStatusUseCase().execute()
        logger.info(f"Model status: {'Running' if status else 'Stopped'}")
        return jsonify({"is_running": status,"status": "Running" if status else "Stopped"}), 200
    except Exception as e:
        logger.error("Error in /model-status endpoint", exc_info=True)
        return jsonify({"error": "Failed to retrieve model status"}), 500
