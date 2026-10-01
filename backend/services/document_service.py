from uuid import uuid4

from backend.schemas.udr import DocumentSource, UdrDocument


SUPPORTED_MIME_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
}
SUPPORTED_TARGET_LANGUAGES = {"hi", "mr"}


class DocumentService:
    def create_initial_udr(
        self,
        *,
        document_type: str,
        source_language: str,
        mime_type: str,
        domain: str,
    ) -> UdrDocument:
        if mime_type not in SUPPORTED_MIME_TYPES:
            raise ValueError(f"Unsupported MIME type: {mime_type}")

        return UdrDocument(
            document_id=uuid4(),
            document_type=document_type,
            source=DocumentSource(
                language=source_language,
                mime_type=mime_type,
            ),
            domain=domain,
            pages=[],
        )
