from flask import jsonify
from app.core.use_cases.start_model_use_case import StartModelUseCase
from app.core.exceptions import ModelAlreadyRunningException

def start_model_controller():
    try:
        use_case = StartModelUseCase()
        response = use_case.execute()
        return jsonify({"message": "Model started successfully", "response": response}), 200
    except ModelAlreadyRunningException as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to start model"}), 500
