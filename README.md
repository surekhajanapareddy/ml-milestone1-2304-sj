# Milestone 1 – Web & Serverless Model Serving

This project demonstrates serving a trained scikit-learn model using two cloud deployment patterns:

    A containerized FastAPI service deployed on Google Cloud Run
    A serverless Cloud Function (Gen 2) implementing the same inference logic

Both deployments use the same trained model artifact, enabling a clear comparison of serving lifecycle, artifact handling, and platform trade-offs.

## 1. Setup Instructions

    Local Environment
    Python 3.11
    pip
    Docker (for Cloud Run)
    Google Cloud SDK (gcloud)

### Project Setup

```bash
git clone https://github.com/surekhajanapareddy/ml-milestone1-2304-sj
cd ml-milestone1-2304-sj
```
Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\Activate
pip install -r requirements.txt
```

Run the FastAPI service locally:

```bash
uvicorn main:app --reload
```

Interactive API documentation:

```bash
http://127.0.0.1:8000/docs
```

## 2. API Usage Examples

### Cloud Run – Prediction

```bash 
POST /predict
```
Request

```bash
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

Response

```bash
{
    "prediction": 0,
    "confidence": 0.9765720577979708
}
```
### Cloud Run – Health Check

```bash
GET /health
```

Response

```bash
{
    "status": "ok"
}
```

### Cloud Function – Prediction

```bash
POST /predict
```

Request

```bash
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

Response

```bash
{
    "prediction": 0
}
```
### Cloud Function – Health Check

```bash
GET ?health=true
```

Response

```bash
{
    "model_loaded": true,
    "status": "ok"
}
```

## 3. Deployment URLs

### Cloud Run (Containerized FastAPI)

```bash
https://iris-fastapi-240926533780.us-central1.run.app
```

#### Available endpoints:

    /predict
    /health
    /docs

### Cloud Function (Gen 2)

```bash
https://us-central1-ml-milestone1-2304-sj.cloudfunctions.net/iris-predict-fn
```

## 4. Lifecycle Explanation

### Model Artifact Lifecycle

    A Logistic Regression model is trained offline on the Iris dataset.
    The trained model is serialized as model.pkl.
    Training and serving are fully decoupled.

### Cloud Run Lifecycle

    The FastAPI application and model artifact are packaged into a Docker image.
    The container reads the serving port from the PORT environment variable.
    The model is loaded once at container startup (cold start).
    Subsequent requests reuse the in-memory model instance.
    Cloud Run manages instance creation, scaling, and shutdown.

### Cloud Functions Lifecycle

    Cloud Functions (Gen 2) expose a single HTTP handler.
    User-managed web servers are not allowed.
    Only files inside the function source directory are deployed.
    The model artifact is loaded once during cold start.
    Each request is stateless and handled independently.

This highlights how artifact visibility and startup behavior differ between container-based and function-based platforms.

## 5. Comparative Analysis

| Aspect                 | Cloud Run                   | Cloud Functions (Gen 2) |
| ---------------------- | --------------------------- | ----------------------- |
| Abstraction            | Container-based service     | Function-based handler  |
| Routing                | Multiple endpoints          | Single handler          |
| Runtime control        | Full control via Docker     | Restricted runtime      |
| Artifact scope         | Entire container filesystem | Source directory only   |
| Health checks          | Explicit `/health` endpoint | Logical health check    |
| Cold start behavior    | Less frequent               | More frequent           |
| Operational complexity | Moderate                    | Low                     |
| Flexibility            | High                        | Lower                   |

### Summary:

Cloud Run provides greater flexibility and runtime control, making it suitable for complex web services. Cloud Functions emphasize simplicity and minimal operational overhead but impose stricter constraints. Both platforms support scalable, stateless inference when designed correctly.

