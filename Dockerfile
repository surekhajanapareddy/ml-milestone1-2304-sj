# ---------- Stage 1: builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies into /install
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ---------- Stage 2: runtime ----------
FROM python:3.11-slim

WORKDIR /app

# Copy only installed python packages
COPY --from=builder /install /usr/local

# Copy app + model
COPY main.py .
COPY model.pkl .

EXPOSE 8080

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
