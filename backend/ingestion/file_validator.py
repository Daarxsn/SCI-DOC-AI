from dataclasses import dataclass

SUPPORTED_MIME_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
}

MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024


@dataclass(frozen=True)
class ValidatedFile:
    filename: str
    mime_type: str
    size_bytes: int


def validate_file_metadata(filename: str, mime_type: str, size_bytes: int) -> ValidatedFile:
    if not filename.strip():
        raise ValueError("filename is required")
    if mime_type not in SUPPORTED_MIME_TYPES:
        raise ValueError(f"unsupported MIME type: {mime_type}")
    if size_bytes <= 0:
        raise ValueError("file must not be empty")
    if size_bytes > MAX_FILE_SIZE_BYTES:
        raise ValueError("file exceeds the 50 MB upload limit")

    return ValidatedFile(
        filename=filename,
        mime_type=mime_type,
        size_bytes=size_bytes,
    )
