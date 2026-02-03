import joblib
import numpy as np

# Load model at import time (best practice for Cloud Functions)
model = joblib.load("model.pkl")

def predict(request):
    request_json = request.get_json(silent=True)

    if not request_json:
        return {"error": "Invalid JSON"}, 400

    try:
        features = np.array([[
            request_json["sepal_length"],
            request_json["sepal_width"],
            request_json["petal_length"],
            request_json["petal_width"]
        ]])

        prediction = int(model.predict(features)[0])
        confidence = float(max(model.predict_proba(features)[0]))

        return {
            "prediction": prediction,
            "confidence": confidence
        }

    except KeyError as e:
        return {"error": f"Missing field: {str(e)}"}, 400
