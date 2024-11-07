from flask import jsonify
from app.core.use_cases.check_model_status_use_case import CheckModelStatusUseCase

def check_model_status_controller():
    try:
        use_case = CheckModelStatusUseCase()
        is_running = use_case.execute()
        print ("esta es un prueba")
        
        status = "encendido" if is_running else "apagado"
        return jsonify({"is_running": is_running, "message": f"El modelo está {status}"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error al verificar el estado del modelo"}), 500
