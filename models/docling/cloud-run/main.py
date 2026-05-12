import functions_framework
from google.cloud import storage
import os

# Suppress PyTorch C++ hardware warnings and force offline mode to use pre-downloaded Docker cache
os.environ["TORCH_CPP_LOG_LEVEL"] = "ERROR"
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["HF_HUB_VERBOSITY"] = "error"

import time
from datetime import datetime
import logging
import torch
torch.backends.nnpack.enabled = False

# Configure production cloud logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("CloudEventarcProcessor")


from docling.document_converter import DocumentConverter

# Initialize Docling and convert the document
converter = DocumentConverter()

# Initialize the GCS client globally for connection pooling
storage_client = storage.Client()

# Read the destination bucket from environment variables
DESTINATION_BUCKET_NAME = os.environ.get("DESTINATION_BUCKET")


@functions_framework.cloud_event
def process_document(cloud_event):
    """Triggered by a change to a Cloud Storage bucket."""
    # 1. Record the start time
    start_epoch = time.perf_counter()
    start_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    data = cloud_event.data
    source_bucket_name = data["bucket"]
    file_name = data["name"]

    logger.info(f"--- Execution Started at {start_utc} ---")
    logger.info(f"Processing file: {file_name} from bucket: {source_bucket_name}")

    if not DESTINATION_BUCKET_NAME:
        logger.error("DESTINATION_BUCKET environment variable is not set.")
        raise ValueError("DESTINATION_BUCKET environment variable is not set.")

    source_bucket = storage_client.bucket(source_bucket_name)
    blob = source_bucket.blob(file_name)

    # Cloud Functions use /tmp for local memory-backed storage
    local_path = f"/tmp/{file_name.replace('/', '_')}"

    try:
        # Determine destination filename
        base_name = os.path.splitext(file_name)[0]
        output_filename = f"{base_name}.md"

        dest_bucket = storage_client.bucket(DESTINATION_BUCKET_NAME)
        dest_blob = dest_bucket.blob(output_filename)

        # Check if document already exists in destination bucket
        if dest_blob.exists():
            logger.info(
                f"Document {output_filename} already exists in destination bucket {DESTINATION_BUCKET_NAME}. Skipping conversion."
            )
            return

        # Download the file locally
        blob.download_to_filename(local_path)

        result = converter.convert(local_path)

        # Export the extracted content to Markdown
        markdown_output = result.document.export_to_markdown()

        # Upload the processed markdown to the destination bucket
        dest_blob.upload_from_string(markdown_output, content_type="text/markdown")

        logger.info(
            f"Successfully uploaded parsed Markdown to {DESTINATION_BUCKET_NAME}/{output_filename}"
        )

    except Exception as e:
        logger.error(f"Error processing {file_name}: {e}", exc_info=True)
        raise e

    finally:
        # Clean up the local memory storage to prevent memory leaks
        if os.path.exists(local_path):
            os.remove(local_path)

        # 2. Record the end time and calculate total elapsed time
        end_epoch = time.perf_counter()
        end_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        total_time = end_epoch - start_epoch

        logger.info(f"--- Execution Ended at {end_utc} ---")
        logger.info(f"Total processing time: {total_time:.2f} seconds")
