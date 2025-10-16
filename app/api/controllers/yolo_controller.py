from flask import request, jsonify, send_file
from ultralytics import YOLO
from collections import Counter
from PIL import Image
import numpy as np
import io, base64, os

# Carga del modelo (una sola vez al iniciar)
MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "YOLO/best.pt")
DEVICE = os.getenv("YOLO_DEVICE", "cpu")  # usa "cpu" si no tenés CUDA
CONF = float(os.getenv("YOLO_CONF", "0.25"))
IOU = float(os.getenv("YOLO_IOU", "0.45"))

model = YOLO(MODEL_PATH)
NAMES = model.names if isinstance(model.names, list) else list(model.names.values())

# Warmup
dummy = np.zeros((640, 640, 3), dtype=np.uint8)
model.predict(dummy, imgsz=640, device=DEVICE, verbose=False)

def _b64_from_pil(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def predict_image():
    """
    POST /api/yolo/predict
    Acepta:
      - form-data: file
      - JSON: {"image_base64": "...", "return_image": true|false}
    Devuelve detecciones + (opcional) imagen anotada en base64.
    """
    try:
        # flag: devolver imagen anotada?
        return_image = False
        if "return_image" in request.args:
            return_image = request.args.get("return_image", "false").lower() == "true"
        else:
            data0 = request.get_json(silent=True) or {}
            if "return_image" in data0:
                return_image = str(data0.get("return_image")).lower() == "true"

        # Obtener imagen
        if "file" in request.files:
            img_bytes = request.files["file"].read()
        else:
            data = request.get_json(silent=True) or {}
            b64 = data.get("image_base64")
            if not b64:
                return jsonify({"error": "Falta imagen en 'file' o 'image_base64'."}), 400
            # soporta "data:image/jpeg;base64,...."
            if "," in b64:
                b64 = b64.split(",", 1)[1]
            img_bytes = base64.b64decode(b64.encode("utf-8"))

        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        np_img = np.array(img)

        # Inferencia YOLO
        results = model.predict(
            source=np_img,
            imgsz=640,
            conf=CONF,
            iou=IOU,
            device=DEVICE,
            verbose=False
        )

        r = results[0]
        detections = []
        for b in r.boxes:
            xyxy = b.xyxy[0].tolist()
            conf = float(b.conf[0].item())
            cls_id = int(b.cls[0].item())
            detections.append({
                "cls": NAMES[cls_id] if 0 <= cls_id < len(NAMES) else str(cls_id),
                "cls_id": cls_id,
                "conf": round(conf, 3),
                "xyxy": [round(float(x), 2) for x in xyxy]
            })

        counts = Counter([d["cls"] for d in detections])

        resp = {
            "detections": detections,
            "counts": dict(counts)
        }

        if return_image:
            plotted = r.plot()               # np array BGR con cajas
            img_rgb = Image.fromarray(plotted[:, :, ::-1])
            resp["image_base64"] = _b64_from_pil(img_rgb)

        return jsonify(resp), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
