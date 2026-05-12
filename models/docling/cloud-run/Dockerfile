# Use a lightweight Python base image
FROM python:3.11-slim

# Install the missing C-libraries required by OCR engines
RUN apt-get update && apt-get install -y \
    libxcb1 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir docling --extra-index-url https://download.pytorch.org/whl/cpu

ENV HF_HOME=/tmp/
ENV TORCH_HOME=/tmp/
ENV DOCLING_ARTIFACTS_PATH=/root/.cache/docling/models

RUN docling-tools models download

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Run the Functions Framework exactly as Cloud Functions does
CMD ["functions-framework", "--target=process_document", "--port=8080"]