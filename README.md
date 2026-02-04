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

The milestone-provided directory structure illustrates a conceptual layout. In practice, Cloud Functions enforce a strict source packaging boundary. Any artifacts required at inference time must be present within the function source directory. As a result, model.pkl is placed inside cloud_function/ to satisfy this constraint.

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

### Artifact Registry Image Reference

The containerized FastAPI service was built locally and pushed to Google Cloud Artifact Registry before deployment to Cloud Run.

Image reference:

```bash
us-central1-docker.pkg.dev/ml-milestone1-2304-sj/ml-models/iris-fastapi:latest
```

Cloud Run pulls this image directly from Artifact Registry during service deployment.

Cloud run URL:

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

### Model–API Interaction

    The trained machine learning model is saved as a file (`model.pkl`) and is used only for prediction. The API does not train the model; it simply loads the already trained model and uses it to make predictions.
    When a request is sent to the API, the input values are read from the request body and converted into the format expected by the model. These values are then passed to the model’s `predict` method. The prediction result is returned to the user as a JSON response.
    In both Cloud Run and Cloud Functions, the model is loaded once when the service starts (cold start) and reused for all future requests handled by the same instance. This keeps the API stateless while improving performance by avoiding repeated model loading.


### Cold Start Behavior and Lifecycle Implications

    A cold start happens when the cloud platform needs to create a new instance to handle a request. During this time, the runtime environment starts up and the trained model (model.pkl) is loaded into memory before the request can be processed.
    In Cloud Run, cold starts are usually less noticeable because container instances can stay alive and handle multiple requests over time. Once the container is running, the model stays in memory and subsequent requests are served faster.
    In Cloud Functions, cold starts can happen more often because function instances are scaled down quickly when there is no traffic. When a new request arrives after idle time, the function has to start again and reload the model, which can add some delay to the first request.
    Overall, both platforms are stateless and load the model during startup, but Cloud Run tends to reuse instances longer, while Cloud Functions focus on simplicity and automatic scaling. This leads to a trade-off between lower latency and ease of deployment when choosing between the two.


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

### Summary

Cloud Run provides greater flexibility and runtime control, making it suitable for complex web services. Cloud Functions emphasize simplicity and minimal operational overhead but impose stricter constraints. Both platforms support scalable, stateless inference when designed correctly.

From a reproducibility perspective, both deployments ensure consistent behavior by reusing the same trained model artifact and pinned
dependencies. Cloud Run achieves reproducibility through containerization, where the runtime environment is fully defined by the Docker image. Cloud Functions provide reproducibility by enforcing a managed runtime and packaging all required artifacts within the function source directory.



