# ---- Build stage ---------------------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

# ---- Runtime stage ---------------------------------------------------------
FROM python:3.11-slim

WORKDIR /app

# Copy installed dependencies from the build stage
COPY --from=builder /root/.local /root/.local

# Copy application source code
COPY . .

# Make sure locally installed packages are on PATH
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
