import base64

from flask import jsonify

from app.core.models.draw_label_data import DrawLabelData
from app.core.models.draw_labels_data import DrawLabelsData, ImageDrawed
from PIL import ImageDraw

class ImageHelper():    
    # Decodifica una imagen en formato base64
    def decode_base64_image(self, base64_str):
        if base64_str.startswith("data:image"):
            base64_str = base64_str.split(",")[1]
        image_data = base64.b64decode(base64_str)
        return image_data
    
    # Dibuja los cuadros delimitadores a la imagen.
    def draw_label_to_image(self, draw_label_data: DrawLabelData):
        left = draw_label_data.box['Left'] * draw_label_data.image.width
        top = draw_label_data.box['Top'] * draw_label_data.image.height
        width = draw_label_data.box['Width'] * draw_label_data.image.width
        height = draw_label_data.box['Height'] * draw_label_data.image.height
        draw_label_data.draw.rectangle([left, top, left + width, top + height], outline=draw_label_data.color, width=3)
        return draw_label_data

    # Dibuja los cuadros delimitadores a la imagen.
    def draw_labels_to_image(self, draw_labels_data: DrawLabelsData):
        try:
            free_count, occupied_count = 0, 0
            draw = ImageDraw.Draw(draw_labels_data.image)
            for label in draw_labels_data.labels:
                label_name = label['Name'].lower()
                color = 'green' if label_name == 'free' else 'red' if label_name == 'occupied' else None
                if color:
                    free_count += (label_name == 'free')
                    occupied_count += (label_name == 'occupied')
                    box = label['Geometry']['BoundingBox']
                    self.draw_label_to_image(
                        DrawLabelData(
                            image=draw_labels_data.image, draw=draw, color=color, box=box
                        )
                    )
            return ImageDrawed(free_spaces=free_count, occupied_spaces= occupied_count, image= draw_labels_data.image)
        except Exception as e:
            return jsonify({"success": False, "error": f"Failed to draw label in image: {e}"}), 500
