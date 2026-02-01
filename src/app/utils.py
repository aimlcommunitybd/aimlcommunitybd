from werkzeug.utils import secure_filename
import os
import uuid
import csv
from datetime import datetime
import structlog
from app import settings

logger = structlog.get_logger(__name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, filename="img"):
    if file and allowed_file(file.filename):
        ext = file.filename.split('.')[-1]
        filename = secure_filename(filename.replace(" ", "_").lower()) + f".{ext}"
        unique_filename = str(uuid.uuid4()) + '_' + filename
        file_path = os.path.join(
            settings.ACTIVITY_IMG_FOLDER, 
            unique_filename
        )
        path_to_save = f"{settings.BASE_DIR}/{file_path}"
        file.save(path_to_save)
        return file_path
    return None

def format_event_date(event_date):
    if not event_date:
        raise ValueError("Event date is required")
    try:
        return datetime.strptime(event_date, '%Y-%m-%dT%H:%M')
    except ValueError as exc:
        raise ValueError(f"Invalid date format. Exc: {exc}")

def delete_file(file_path):
    logger.info("[Delete] file", file_path=file_path)
    if not file_path:
        logger.warning("No file path provided to delete")
        return False
    if not file_path.startswith(settings.BASE_DIR):
        file_path = f"{settings.BASE_DIR}/{file_path}"
    if os.path.exists(file_path):
        logger.info("File found, deleting...", file_path=file_path)
        os.remove(file_path)
        return True
    logger.warning("File not found, cannot delete", file_path=file_path)
    return False


def get_rows_from_csv(filename:str) -> list[dict]:
    """
    Convert Supabase CSV file to a list of row dictionaries.
    It can be used during development and testing instead of connecting to Supabase.
    
    Args:
        filename: Full path to the CSV file.
        output_format: Python list format
    
    Returns:
        List of dictionaries where each dictionary represents a row
    """
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        rows = list(csv_reader)
    return rows