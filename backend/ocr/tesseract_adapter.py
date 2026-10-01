from pathlib import Path

from backend.ocr.base import OcrAdapter
from backend.ocr.models import OcrBlock, OcrPageResult, OcrWord


class TesseractAdapter(OcrAdapter):
    name = "tesseract"

    def __init__(self, language: str = "eng") -> None:
        self.language = language

    def extract(self, image_path: str | Path) -> OcrPageResult:
        try:
            import pytesseract
            from PIL import Image
        except ImportError as exc:
            raise RuntimeError("pytesseract and Pillow are required for Tesseract OCR") from exc

        image_path = Path(image_path)
        with Image.open(image_path) as image:
            width, height = image.size
            data = pytesseract.image_to_data(
                image,
                lang=self.language,
                output_type=pytesseract.Output.DICT,
                config="--psm 6",
            )

        grouped: dict[tuple[int, int, int], list[OcrWord]] = {}

        count = len(data["text"])
        for index in range(count):
            text = data["text"][index].strip()
            try:
                confidence = float(data["conf"][index])
            except (TypeError, ValueError):
                confidence = -1

            if not text or confidence < 0:
                continue

            word = OcrWord(
                text=text,
                confidence=min(confidence / 100, 1),
                x=max(0, int(data["left"][index])),
                y=max(0, int(data["top"][index])),
                width=max(0, int(data["width"][index])),
                height=max(0, int(data["height"][index])),
            )

            key = (
                int(data["block_num"][index]),
                int(data["par_num"][index]),
                int(data["line_num"][index]),
            )
            grouped.setdefault(key, []).append(word)

        blocks: list[OcrBlock] = []
        for order, words in enumerate(grouped.values()):
            x = min(word.x for word in words)
            y = min(word.y for word in words)
            right = max(word.x + word.width for word in words)
            bottom = max(word.y + word.height for word in words)

            blocks.append(
                OcrBlock(
                    text=" ".join(word.text for word in words),
                    confidence=sum(word.confidence for word in words) / len(words),
                    x=x,
                    y=y,
                    width=right - x,
                    height=bottom - y,
                    words=words,
                    reading_order=order,
                )
            )

        return OcrPageResult(
            width=width,
            height=height,
            blocks=blocks,
            engine=self.name,
            engine_version=getattr(pytesseract, "__version__", None),
        )
