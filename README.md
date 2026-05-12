# 🚀 Enterprise Advanced OCR Suite

An engineering repository dedicated to designing, benchmarking, and deploying cutting-edge Document Intelligence and Optical Character Recognition (OCR) pipelines. 

This repository focuses on integrating heavy machine learning models (such as **Docling**, **PyTorch**, and **RapidOCR**) across highly scaled **Google Cloud Platform (GCP)** architectures and local processing environments.

---

## 📁 Repository Architecture

The project codebase is organized into focused implementation modules under the `models/` directory:

```
ai-advanced-ocr/
├── models/
│   └── docling/
│       ├── main.py              # 💻 Local bulk multi-threaded converter
│       ├── README.md            # Local usage benchmarks & pricing
│       └── cloud-run/           # ☁️ Enterprise Cloud Run / Eventarc Processor
│           ├── main.py          # Cloud Functions framework handler
│           ├── README.md        # Eventarc architectures & shell flags
│           └── deploy.sh        # Secure deployment automation script
```

---

## 🧠 Deep Learning Engines & Modules

- **[Docling](https://github.com/DS4SD/docling)**: Advanced PDF Document Layout Analysis and Structure Recognition utilizing deep learning components (`TableFormer` grids, object detection boundaries).
- **PyTorch Compute Engine**: Optimized tensor math backends operating natively on CPU core structures.
- **RapidOCR**: High-throughput text extractor modules configured to run silently across underlying PyTorch compute backbones.

---

## 💡 Key Production Learnings & Best Practices

Through comprehensive load testing and operational alignment, this repository establishes definitive architectural standards for production ML deployments:

1. **Cloud Run Resource Contention**: PyTorch multi-threaded execution loops heavily contend for shared virtual CPUs. Setting `--concurrency 1` completely isolates memory and execution threads per document trigger, accelerating real-world throughput without thread starvation.
2. **Pre-Loading Remote Model Artifacts**: Embedding ML snapshots inside the base container layers paired with silent online lazy loading (`HF_HUB_OFFLINE=0`) ensures rapid cold-starts while guaranteeing seamless compatibility across highly specialized document formats.
3. **Absolute Execution Silence**: Explicitly muting low-level hardware compatibility traces (`TORCH_CPP_LOG_LEVEL=ERROR`) and overriding third-party library loggers (`logging.getLogger('rapidocr_torch').setLevel(...)`) prevents severe log stream pollution and controls Cloud Logging costs.
4. **Data Privacy Hardening**: Using dynamic hash filenames (SHA-256) for runtime storage outputs paired with complete gitignore obfuscation rules permanently protects confidential operational documents from version control exposure.

---

## 🧭 Quick Navigation

- 📖 **[Explore the Local Batch Processor Benchmarks](file:///usr/local/google/home/vieiravitor/workspace/opensource-google/ai-advanced-ocr/models/docling/README.md)**
- 📖 **[Read the Cloud Eventarc OCR Processor Guide](file:///usr/local/google/home/vieiravitor/workspace/opensource-google/ai-advanced-ocr/models/docling/cloud-run/README.md)**