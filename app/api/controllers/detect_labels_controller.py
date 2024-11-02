from flask import request, jsonify
from app.core.use_cases.detect_label_use_case import DetectLabelsUseCase

def detect_labels_controller():
    # Verifica que haya un archivo en la solicitud
    if 'image' not in request.files:
        return jsonify({'error': 'No se encontró ninguna imagen'}), 400
    
    image = request.files['image']
    image_bytes = image.read()

    try:
        use_case = DetectLabelsUseCase()
        labels = use_case.execute(image_bytes)
        return jsonify({'labels': labels}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Error al procesar la imagen'}), 500
