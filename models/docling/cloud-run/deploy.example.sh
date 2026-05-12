#!/usr/bin/env bash

# --- DEPLOYMENT CONFIGURATION ---
SERVICE_NAME="docling-ocr-processor"
REGION="us-central1"
INPUT_BUCKET="your-input-bucket-name"
OUTPUT_BUCKET="your-output-bucket-name"
HF_TOKEN="your_huggingface_token_here"
SERVICE_ACCOUNT="your-project-number-compute@developer.gserviceaccount.com"
# --------------------------------

# 1. Deploy the container service to Cloud Run
gcloud run deploy "${SERVICE_NAME}" \
  --source . \
  --region "${REGION}" \
  --cpu 8 \
  --memory 8Gi \
  --concurrency 1 \
  --cpu-boost \
  --timeout 890s \
  --set-env-vars DESTINATION_BUCKET="${OUTPUT_BUCKET}",USE_NNPACK=0 \
  --set-build-env-vars HF_TOKEN="${HF_TOKEN}" \
  --no-allow-unauthenticated

# 2. Grant internal access permissions
gcloud run services add-iam-policy-binding "${SERVICE_NAME}" \
  --region="${REGION}" \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/run.invoker"

# 3. Create the Eventarc trigger for bucket file finalized events
gcloud eventarc triggers create docling-gcs-trigger \
  --location="${REGION}" \
  --destination-run-service="${SERVICE_NAME}" \
  --destination-run-region="${REGION}" \
  --event-filters="type=google.cloud.storage.object.v1.finalized" \
  --event-filters="bucket=${INPUT_BUCKET}" \
  --service-account="${SERVICE_ACCOUNT}"
