from flask import jsonify
from app.core.use_cases.stop_model_use_case import StopModelUseCase
from app.core.exceptions import ModelAlreadyStoppedException

def stop_model_controller():
    try:
        use_case = StopModelUseCase()
        response = use_case.execute()
        return jsonify({"message": "Model stopped successfully", "response": response}), 200
    except ModelAlreadyStoppedException as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to stop model"}), 500
