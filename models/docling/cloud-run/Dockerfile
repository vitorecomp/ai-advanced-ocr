# Use a lightweight Python base image
FROM python:3.11-slim

# Install the missing C-libraries required by OCR engines
RUN apt-get update && apt-get install -y \
    libxcb1 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- NEW: Pre-download Hugging Face Models ---
# 1. Set the Hugging Face cache directory inside the image
ENV HF_HOME=/opt/huggingface

# 2. Accept the token securely as a build argument
ARG HF_TOKEN

# 3. Pre-download models by initializing the DocumentConverter
RUN HF_TOKEN=${HF_TOKEN} python -c "import torch; torch.backends.nnpack.enabled = False; from docling.document_converter import DocumentConverter; DocumentConverter()"
# ---------------------------------------------


# Copy the rest of your application code
COPY . .

# Run the Functions Framework exactly as Cloud Functions does
CMD ["functions-framework", "--target=process_document", "--port=8080"]