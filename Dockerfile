# Multi-stage build for Hugging Face Space
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Python backend stage
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy app.py entry point
COPY app.py ./

# Copy built frontend from builder stage
COPY --from=frontend-builder /app/frontend/build ./static

# Create directory for models (will be downloaded from HF Hub)
RUN mkdir -p ./models

# Expose port (HF Spaces uses PORT env var)
ENV PORT=7860
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]

