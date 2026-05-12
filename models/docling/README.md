# 📄 Docling Local Batch Processor

A highly optimized Python tool for running bulk document-to-Markdown conversions locally using the **Docling** advanced document parser. 

This utility maximizes your host machine's performance while guaranteeing perfectly formatted output files and an ultra-clean, noise-free execution log.

---

## ✨ Core Features & Optimizations

- **🚀 Maximum CPU Multi-Threading**: Dynamically forces underlying machine learning engines (PyTorch / OpenMP) to utilize all available physical CPU cores during intra-op tensor operations.
- **🤫 Absolute Noise Suppression**: Explicitly quiets verbose initialization statements from third-party dependency sub-modules (like `rapidocr_torch`) and silences hardware compatibility warning logs.
- **📦 Resilient Offline Caching**: Operates primarily from pre-cached model weights while quietly allowing lazy updates for missing, highly specialized document structures on the fly.
- **📊 Throughput Metrics**: Logs extracted page counts in real-time and concludes batches with calculated average durations per document and per page.

---

## 💻 Usage Instructions

1. **Setup Folder Structure**: Place all your target input files (`.pdf`, `.docx`, etc.) inside the default `docs/` input directory.
2. **Execute Conversion**:
   ```bash
   python main.py
   ```
3. **View Results**: Structured Markdown exports will appear instantly inside the `doc-output/` folder.

---

## 💰 Cost & Pricing Analysis

Based on reference Google Cloud infrastructure metrics, running these deep learning pipelines in production scales highly efficiently:

- **Cost per 1,000 Documents**: `~$13.92`
- **Cost per Document**: `~$0.01392`
- **Cost per Page**: `~$0.0000732`

🔗 [View Complete GCP Pricing Calculator Estimation](https://cloud.google.com/products/calculator?hl=en&dl=CjhDaVE1TWpaaE16QTNaaTFqWldKbExUUTVZV1V0T0dRd05DMWhZekF6WXpZd01UWTJaR1FRQVE9PRAcGiQ2RkUzNjIzMC02MTM4LTQxOTMtOTMwRi04MjI2NThFMkJBNTk)

---

## ⏱️ Performance Benchmark Table

Below are actual local execution reference timings across a sample set of 16 document structures. *(File names have been converted to anonymous hashes to preserve data privacy).*

| Anonymized Document Hash | Pages | Conversion Time | Export Time | Total Time |
| :--- | :---: | :---: | :---: | :---: |
| `doc_3f8e2d1a.pdf` | `1` | 8.44s | 0.00s | **8.44s** |
| `doc_7b4c9f0e.pdf` | `1` | 10.11s | 0.00s | **10.11s** |
| `doc_1a2b3c4d.pdf` | `1` | 11.04s | 0.00s | **11.04s** |
| `doc_9d8e7f6a.pdf` | `2` | 16.68s | 0.00s | **16.69s** |
| `doc_5c6b7a8f.pdf` | `6` | 47.11s | 0.01s | **47.12s** |
| `doc_e4f3d2c1.pdf` | `7` | 88.35s | 0.02s | **88.37s** |
| `doc_b1a2f3e4.pdf` | `7` | 91.81s | 0.02s | **91.83s** |
| `doc_0f9e8d7c.pdf` | `8` | 110.92s | 0.03s | **110.96s** |
| `doc_4d3c2b1a.pdf` | `8` | 111.51s | 0.04s | **111.54s** |
| `doc_8a7b6c5d.pdf` | `8` | 111.54s | 0.04s | **111.57s** |
| `doc_c1d2e3f4.pdf` | `8` | 111.65s | 0.04s | **111.69s** |
| `doc_f5e4d3c2.pdf` | `8` | 114.10s | 0.05s | **114.15s** |
| `doc_2b3a4f5e.pdf` | `8` | 116.40s | 0.03s | **116.44s** |
| `doc_6e7f8a9b.pdf` | `11` | 161.48s | 0.01s | **161.49s** |
| `doc_a9b8c7d6.pdf` | `10` | 167.04s | 0.02s | **167.05s** |
| `doc_d4c3b2a1.pdf` | `46` | 730.79s | 0.15s | **730.94s** |

---

## 📈 Aggregate Performance Summary

| Metric | Benchmark Measurement | Notes |
| :--- | :---: | :--- |
| **Total Batch Size** | `16 documents` | Comprehensive sample set |
| **Total Parsed Pages** | `140 pages` | Successfully extracted across batch |
| **Total Cumulative Processing Time** | `2,009.44 seconds` | `~33.5 minutes` gross execution duration |
| **Average Processing Speed per Document** | `125.59 seconds / document` | Mean document completion rate |
| **Average Processing Speed per Page** | `14.35 seconds / page` | Calculated aggregate page velocity |
