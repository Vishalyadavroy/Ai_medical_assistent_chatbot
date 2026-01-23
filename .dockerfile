FROM python:3.11-slim

WORKDIR /AI_CHATBOT

# Install system dependencies and upgrade pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

# Copy and install requirements first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000

# Run uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
