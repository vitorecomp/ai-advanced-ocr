import os

# Allow silent online lazy downloads for any un-cached runtime format models
os.environ["HF_HUB_OFFLINE"] = "0"
os.environ["HF_HUB_VERBOSITY"] = "error"

import time
import traceback
from pathlib import Path
import logging
import torch

# Silence third-party INFO logging from RapidOCR and Hugging Face
logging.getLogger("RapidOCR").setLevel(logging.WARNING)
logging.getLogger("rapidocr_onnxruntime").setLevel(logging.WARNING)
logging.getLogger("rapidocr_pdf").setLevel(logging.WARNING)
logging.getLogger("rapidocr_torch").setLevel(logging.WARNING)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

# Maximize PyTorch intra-op threading for underlying model execution
max_threads = os.cpu_count() or 4
torch.set_num_threads(max_threads)
os.environ["OMP_NUM_THREADS"] = str(max_threads)
# Suppress PyTorch C++ hardware warnings
os.environ["TORCH_CPP_LOG_LEVEL"] = "ERROR"

from docling.document_converter import DocumentConverter

converter = DocumentConverter()


def process_folder(input_folder_name="docs", output_folder_name="doc-output"):
    # Define input and output paths
    in_dir = Path(input_folder_name)
    out_dir = Path(output_folder_name)

    # Create the output directory if it doesn't exist
    out_dir.mkdir(parents=True, exist_ok=True)

    # Ensure the input directory exists
    if not in_dir.exists():
        print(f"Error: The input folder '{input_folder_name}' does not exist.")
        return

    print(
        f"Starting conversion of files in '{input_folder_name}' to '{output_folder_name}'...\n"
    )

    success_count = 0
    failure_count = 0
    total_pages = 0
    total_doc_time_sum = 0.0

    # Start timer for the entire batch
    batch_start_time = time.perf_counter()

    for file_path in in_dir.glob("*.*"):
        # Skip directories
        if file_path.is_dir():
            continue

        print(f"Processing: {file_path.name}...")

        # Start timer for the individual document
        doc_start_time = time.perf_counter()

        try:
            # 1. Convert the document
            conv_start = time.perf_counter()
            result = converter.convert(file_path)
            conv_end = time.perf_counter()

            # 2. Export the structured document to Markdown
            export_start = time.perf_counter()
            markdown_text = result.document.export_to_markdown()
            export_end = time.perf_counter()

            # Define the output file path using a secure SHA-256 hash for anonymity
            import hashlib

            file_hash = hashlib.sha256(
                file_path.stem.encode("utf-8")
            ).hexdigest()[:12]
            output_file = out_dir / f"{file_hash}.md"

            # Write the Markdown to the output folder
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(markdown_text)

            doc_end_time = time.perf_counter()

            # Calculate and log timings
            total_doc_time = doc_end_time - doc_start_time
            conv_time = conv_end - conv_start
            export_time = export_end - export_start

            # Extract page count safely
            num_pages = (
                len(result.document.pages)
                if hasattr(result.document, "pages") and result.document.pages
                else 1
            )

            total_pages += num_pages
            total_doc_time_sum += total_doc_time
            success_count += 1

            print(f"  -> Pages: {num_pages}")
            print(f"  -> Saved as: {output_file.name}")
            print(
                f"  -> [Timing] Total: {total_doc_time:.2f}s (Conversion: {conv_time:.2f}s | Export: {export_time:.2f}s)"
            )

        except Exception as e:
            doc_end_time = time.perf_counter()
            print(f"  -> Error processing {file_path.name}: {e}")
            print(f"  -> [Timing] Failed after {doc_end_time - doc_start_time:.2f}s")
            # print(traceback.format_exc())
            failure_count += 1

    batch_end_time = time.perf_counter()

    print("\n--- Summary ---")
    print(f"Successfully converted: {success_count} files")
    print(f"Failed conversions: {failure_count} files")
    print(f"Total batch time: {batch_end_time - batch_start_time:.2f} seconds")
    if success_count > 0:
        avg_doc_time = total_doc_time_sum / success_count
        print(f"Average time per document: {avg_doc_time:.2f} seconds")
    if total_pages > 0:
        avg_page_time = total_doc_time_sum / total_pages
        print(f"Average time per page: {avg_page_time:.2f} seconds")


if __name__ == "__main__":
    process_folder("docs", "doc-output")
