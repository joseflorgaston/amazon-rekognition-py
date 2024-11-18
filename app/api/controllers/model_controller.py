import base64
import io
from flask import jsonify
from PIL import Image, ImageDraw, UnidentifiedImageError
from app.config.logging_config import logger
from app.core.helpers.image_helper import ImageHelper
from app.core.use_cases.model_use_cases.start_model_use_case import StartModelUseCase
from app.core.use_cases.model_use_cases.stop_model_use_case import StopModelUseCase
from app.core.use_cases.model_use_cases.check_model_status_use_case import CheckModelStatusUseCase
from app.core.exceptions import ModelAlreadyRunningException, ModelAlreadyStoppedException
from app.core.use_cases.model_use_cases.detect_label_use_case import DetectLabelsUseCase

class ModelController:
    @staticmethod
    def detect_labels(data):
        if 'image' not in data:
            return jsonify({"success": False, "error": "No image data provided"}), 400

        base64_str = data['image']
        if base64_str.startswith("data:image"):
            base64_str = base64_str.split(",")[1]
        image_data = base64.b64decode(base64_str)

        try:
            image = Image.open(io.BytesIO(image_data))
        except UnidentifiedImageError as e:
            print(e)
            return jsonify({"success": False, "error": "Failed to process image"}), 400

        labels = DetectLabelsUseCase().execute(image_data)
        free_count, occupied_count = 0, 0
        draw = ImageDraw.Draw(image)

        for label in labels:
            label_name = label['Name'].lower()
            color = 'green' if label_name == 'free' else 'red' if label_name == 'occupied' else None
            if color:
                free_count += (label_name == 'free')
                occupied_count += (label_name == 'occupied')
                box = label['Geometry']['BoundingBox']
                ImageHelper.draw_label_to_image(image, draw, color, box)

                

        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return jsonify({
            "success": True,
            "image": img_base64,
            "free_spaces": free_count,
            "occupied_spaces": occupied_count
        }), 200
    
    @staticmethod
    def start_model():
        return StartModelUseCase().execute()

    @staticmethod
    def stop_model():
        return StopModelUseCase().execute()

    @staticmethod
    def model_status():
        return CheckModelStatusUseCase().execute()
