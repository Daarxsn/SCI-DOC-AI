from pathlib import Path

from backend.ocr.base import OcrAdapter
from backend.ocr.models import OcrBlock, OcrPageResult, OcrWord


class PaddleOcrAdapter(OcrAdapter):
    """PaddleOCR-backed production OCR adapter."""

    name = "paddleocr"

    def __init__(self, language: str = "en", use_angle_cls: bool = True) -> None:
        self.language = language
        self.use_angle_cls = use_angle_cls
        self._engine = None

    def _get_engine(self):
        if self._engine is None:
            try:
                from paddleocr import PaddleOCR
            except ImportError as exc:
                raise RuntimeError(
                    "PaddleOCR is required for the paddleocr adapter."
                ) from exc
            self._engine = PaddleOCR(
                lang=self.language,
                use_angle_cls=self.use_angle_cls,
                show_log=False,
            )
        return self._engine

    def extract(self, image_path: str | Path) -> OcrPageResult:
        try:
            from PIL import Image
        except ImportError as exc:
            raise RuntimeError("Pillow is required for PaddleOCR OCR") from exc

        image_path = Path(image_path)
        with Image.open(image_path) as image:
            width, height = image.size

        result = self._get_engine().ocr(str(image_path), cls=self.use_angle_cls)
        lines = result[0] if result else []
        words: list[OcrWord] = []

        for line in lines or []:
            if not line or len(line) < 2:
                continue
            polygon, text_info = line[0], line[1]
            text, confidence = text_info
            if not text:
                continue

            xs = [float(point[0]) for point in polygon]
            ys = [float(point[1]) for point in polygon]
            x = max(0.0, min(xs))
            y = max(0.0, min(ys))
            right = min(float(width), max(xs))
            bottom = min(float(height), max(ys))

            words.append(
                OcrWord(
                    text=str(text).strip(),
                    confidence=max(0.0, min(float(confidence), 1.0)),
                    x=x,
                    y=y,
                    width=max(0.0, right - x),
                    height=max(0.0, bottom - y),
                )
            )

        blocks = [
            OcrBlock(
                text=word.text,
                confidence=word.confidence,
                x=word.x,
                y=word.y,
                width=word.width,
                height=word.height,
                words=[word],
                reading_order=index,
            )
            for index, word in enumerate(words)
        ]

        return OcrPageResult(
            width=width,
            height=height,
            blocks=blocks,
            engine=self.name,
            engine_version=self._version(),
        )

    def _version(self) -> str | None:
        try:
            import paddleocr
            return getattr(paddleocr, "__version__", None)
        except ImportError:
            return None
