import os
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.config import settings

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


def save_upload_file(file: UploadFile, subfolder: str) -> str:
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"File type '{ext}' is not allowed.")

    dest_dir = Path(settings.UPLOAD_DIR) / subfolder
    dest_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4().hex}{ext}"
    dest_path = dest_dir / filename

    content = file.file.read()
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise ValueError("File size exceeds the 5 MB limit.")

    dest_path.write_bytes(content)
    return str(Path(subfolder) / filename)


def delete_file(relative_path: str) -> None:
    full_path = Path(settings.UPLOAD_DIR) / relative_path
    if full_path.exists():
        full_path.unlink()
