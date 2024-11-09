import base64
import io
from PIL import Image, ImageDraw, UnidentifiedImageError
from flask import jsonify
from app.core.use_cases.detect_label_use_case import DetectLabelsUseCase

class DetectLabelsController:
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
                left = box['Left'] * image.width
                top = box['Top'] * image.height
                width = box['Width'] * image.width
                height = box['Height'] * image.height
                draw.rectangle([left, top, left + width, top + height], outline=color, width=3)

        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return jsonify({
            "success": True,
            "image": img_base64,
            "free_spaces": free_count,
            "occupied_spaces": occupied_count
        }), 200
