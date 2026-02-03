# Milestone 1 – Web & Serverless Model Serving

## Overview
This project demonstrates the deployment of a trained scikit-learn model using two serving patterns:
1. A containerized FastAPI service deployed on Google Cloud Run
2. A serverless Google Cloud Function implementing the same inference logic

The goal is to compare lifecycle behavior, artifact management, latency characteristics, and reproducibility across deployment patterns.

---

## Model Artifact
A logistic regression model trained on the Iris dataset was saved as a serialized artifact (`model.pkl`).  
The model is trained offline and loaded by the serving layer for inference only, reflecting a clear separation between training and serving stages of the ML lifecycle.

---

## Local FastAPI Service

### Architecture
- FastAPI provides the web serving layer
- Pydantic enforces request and response schema validation
- The trained model artifact is loaded once at application startup and reused for all prediction requests

### Endpoints
- `POST /predict` – Accepts feature inputs and returns a prediction with confidence
- `GET /health` – Service health check endpoint

### Running Locally
```bash
uvicorn main:app --reload

```
### Interactive API documentation is available at

http://127.0.0.1:8000/docs


## Cloud Run Deployment

The FastAPI service was containerized using Docker and pushed to Google Cloud Artifact Registry.  
It was then deployed to Google Cloud Run as a fully managed, serverless container service.

- The container reads the serving port from the `PORT` environment variable, ensuring Cloud Run compatibility.
- The trained model artifact is loaded at container startup and reused across requests.
- Cloud Run handles HTTPS, autoscaling, and instance lifecycle management.

### Live Service URL
https://iris-fastapi-501878510537.us-central1.run.app

### Endpoints
- `GET /health`
- `POST /predict`
- `GET /docs`
