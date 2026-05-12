# ☁️ Docling Cloud Eventarc OCR Processor

An enterprise-grade, highly optimized Google Cloud deployment package for automatically processing document uploads using the **Docling** advanced document converter.

Designed to trigger instantly on Google Cloud Storage uploads via **Eventarc**, this service leverages containerized Cloud Run environments powered by the Functions Framework to seamlessly parse PDFs, Word files, and presentations into clean, structured Markdown.

---

## 🏛️ System Architecture

```
[Client Uploads PDF] 
       │
       ▼
[Google Cloud Storage: Input Bucket]
       │
       ▼ (Eventarc Finalized Trigger)
[Cloud Run Service: docling-ocr-processor]
       │ (PyTorch Intra-Op Inference)
       ▼
[Structured Markdown Export]
       │
       ▼
[Google Cloud Storage: Output Bucket]
```

---

## ✨ Enterprise Performance Optimizations

- **⚡ Concurrency Isolation (`--concurrency 1`)**: Cloud Run instances are constrained to process exactly one document at a time. This dedicates the full, undivided compute power of all allocated CPUs (e.g. 8 vCPUs) directly to PyTorch intra-op thread processing, preventing severe context switching and thread starvation.
- **🚀 Startup Acceleration (`--cpu-boost`)**: Dynamically allocates bonus CPU compute during container cold-starts to drastically speed up Hugging Face model initializations.
- **📦 Resilient Remote Caching**: Pre-downloads baseline machine learning weights directly into the container image layer, while quietly permitting lazy fetching for highly complex or optional layout formats without crashing.
- **🤫 Silent Execution**: Natively silences hardware compatibility notices (`TORCH_CPP_LOG_LEVEL=ERROR`) and third-party engine output logs (`RapidOCR`) to preserve a pristine Google Cloud Logging trace.

---

## ⚙️ Configuration & Environment Variables

The service relies on the following critical top-level shell variables defined in your deployment header:

| Variable | Type | Description |
| :--- | :---: | :--- |
| `SERVICE_NAME` | Shell Variable | Name of the deployed Cloud Run service |
| `REGION` | Shell Variable | Target GCP execution region (e.g. `us-central1`) |
| `INPUT_BUCKET` | Shell Variable | Source bucket monitored by Eventarc triggers |
| `OUTPUT_BUCKET` | Runtime Env Var | Target bucket for parsed `.md` exports (`DESTINATION_BUCKET`) |
| `HF_TOKEN` | Build Env Var | Secret Hugging Face authorization token for accessing gate models |

---

## 🚀 Deployment Guide

1. **Configure Secrets**: Duplicate the reference script and customize your project values:
   ```bash
   cp deploy.sh.example deploy.sh
   ```
2. **Execute Deployment**: Run the automated deployment package (requires authenticated `gcloud` access):
   ```bash
   ./deploy.sh
   ```
3. **Verify Integration**: Upload any document to your input bucket and monitor your Cloud Run service logs to see the automatic Markdown generation.
