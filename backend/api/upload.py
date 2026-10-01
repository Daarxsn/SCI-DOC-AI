from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.ingestion.processor import IngestionProcessor

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])
processor = IngestionProcessor()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)) -> dict:
    if not file.filename:
        raise HTTPException(status_code=400, detail="filename is required")

    content = await file.read()

    try:
        with NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp:
            temp.write(content)
            temp_path = temp.name

        pages = processor.inspect(
            path=temp_path,
            filename=file.filename,
            mime_type=file.content_type or "application/octet-stream",
            size_bytes=len(content),
        )
    except ValueError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    finally:
        try:
            Path(temp_path).unlink()
        except (UnboundLocalError, FileNotFoundError):
            pass

    return {
        "status": "accepted",
        "filename": file.filename,
        "mime_type": file.content_type,
        "size_bytes": len(content),
        "pages": [page.__dict__ for page in pages],
    }
