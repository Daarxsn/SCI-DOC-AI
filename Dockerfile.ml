FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV MODEL_CACHE_DIR=/model-cache
ENV HF_HOME=/model-cache/huggingface
ENV TRANSFORMERS_CACHE=/model-cache/huggingface
COPY backend/requirements.txt /app/backend/requirements.txt
COPY requirements-p1.txt /app/requirements-p1.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt && pip install --no-cache-dir -r /app/requirements-p1.txt
COPY backend /app/backend
COPY tests /app/tests
COPY pytest.ini /app/pytest.ini
RUN mkdir -p /model-cache
VOLUME ["/model-cache"]
EXPOSE 8000
CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
