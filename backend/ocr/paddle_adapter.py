from pathlib import Path

from backend.ocr.base import OcrAdapter
from backend.ocr.models import OcrBlock, OcrPageResult, OcrWord


class PaddleOcrAdapter(OcrAdapter):
    """PaddleOCR adapter supporting both legacy OCR and current predict APIs."""

    name = "paddleocr"

    def __init__(self, language: str = "en", use_angle_cls: bool = True, device: str = "auto") -> None:
        self.language = language
        self.use_angle_cls = use_angle_cls
        self.device = device
        self._engine = None

    def _get_engine(self):
        if self._engine is None:
            try:
                from paddleocr import PaddleOCR
            except ImportError as exc:
                raise RuntimeError("PaddleOCR and PaddlePaddle are required.") from exc

            kwargs = {"lang": self.language}
            if self.device != "auto":
                kwargs["device"] = self.device

            try:
                self._engine = PaddleOCR(**kwargs)
            except TypeError:
                kwargs.pop("device", None)
                kwargs["use_angle_cls"] = self.use_angle_cls
                kwargs["show_log"] = False
                self._engine = PaddleOCR(**kwargs)
        return self._engine

    @staticmethod
    def _polygon_to_bbox(polygon, width: int, height: int):
        xs = [float(point[0]) for point in polygon]
        ys = [float(point[1]) for point in polygon]
        x = max(0.0, min(xs))
        y = max(0.0, min(ys))
        right = min(float(width), max(xs))
        bottom = min(float(height), max(ys))
        return x, y, max(0.0, right - x), max(0.0, bottom - y)

    def _legacy_result(self, result, width: int, height: int):
        lines = result[0] if result else []
        words = []
        for line in lines or []:
            if not line or len(line) < 2:
                continue
            polygon, text_info = line[0], line[1]
            text, confidence = text_info
            if not text:
                continue
            x, y, box_w, box_h = self._polygon_to_bbox(polygon, width, height)
            words.append(OcrWord(text=str(text).strip(), confidence=float(confidence), x=x, y=y, width=box_w, height=box_h))
        return words

    def _modern_result(self, result, width: int, height: int):
        data = result
        if hasattr(result, "json"):
            try:
                data = result.json
                if callable(data):
                    data = data()
            except Exception:
                data = result
        if isinstance(data, dict) and "res" in data:
            data = data["res"]

        texts = getattr(result, "rec_texts", None) or (data.get("rec_texts", []) if isinstance(data, dict) else [])
        scores = getattr(result, "rec_scores", None) or (data.get("rec_scores", []) if isinstance(data, dict) else [])
        polys = getattr(result, "rec_polys", None) or (data.get("rec_polys", []) if isinstance(data, dict) else [])
        boxes = getattr(result, "rec_boxes", None) or (data.get("rec_boxes", []) if isinstance(data, dict) else [])

        words = []
        for index, text in enumerate(texts or []):
            if not str(text).strip():
                continue
            confidence = float(scores[index]) if index < len(scores or []) else 0.5
            polygon = polys[index] if index < len(polys or []) else None
            if polygon is not None:
                x, y, box_w, box_h = self._polygon_to_bbox(polygon, width, height)
            elif index < len(boxes or []):
                box = boxes[index]
                x, y, right, bottom = map(float, box[:4])
                x, y, box_w, box_h = x, y, max(0, right - x), max(0, bottom - y)
            else:
                x = y = box_w = box_h = 0.0
            words.append(OcrWord(text=str(text).strip(), confidence=max(0, min(confidence, 1)), x=x, y=y, width=box_w, height=box_h))
        return words

    def extract(self, image_path: str | Path) -> OcrPageResult:
        try:
            from PIL import Image
        except ImportError as exc:
            raise RuntimeError("Pillow is required for PaddleOCR OCR") from exc

        image_path = Path(image_path)
        with Image.open(image_path) as image:
            width, height = image.size

        engine = self._get_engine()
        if hasattr(engine, "predict"):
            results = list(engine.predict(str(image_path)))
            words = self._modern_result(results[0], width, height) if results else []
        else:
            result = engine.ocr(str(image_path), cls=self.use_angle_cls)
            words = self._legacy_result(result, width, height)

        words.sort(key=lambda word: (word.y, word.x))
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
