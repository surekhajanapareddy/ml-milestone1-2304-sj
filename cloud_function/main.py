import os
import joblib
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
model = joblib.load(MODEL_PATH)

def predict(request):
    # ---------- HEALTH CHECK ----------
    if request.method == "GET":
        if request.args and request.args.get("health") == "true":
            return {
                "status": "ok",
                "model_loaded": True
            }
        return ("Not Found", 404)

    # ---------- PREDICTION ----------
    request_json = request.get_json(silent=True)

    if request_json is None:
        return ("Invalid or missing JSON payload", 400)

    try:
        features = np.array([[
            float(request_json["sepal_length"]),
            float(request_json["sepal_width"]),
            float(request_json["petal_length"]),
            float(request_json["petal_width"])
        ]])

        prediction = int(model.predict(features)[0])

        return {
            "prediction": prediction
        }

    except KeyError as e:
        return (f"Missing field: {str(e)}", 400)

    except ValueError as e:
        return (f"Invalid input: {str(e)}", 400)

    except Exception as e:
        return (f"Internal error: {str(e)}", 500)
