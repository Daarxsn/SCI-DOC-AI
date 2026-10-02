from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from backend.ocr.base import OcrAdapter

@dataclass
class OcrComparison:
    provider: str
    elapsed_seconds: float
    text: str
    average_confidence: float
    block_count: int

def compare_ocr(adapters: list[OcrAdapter], image_path: str | Path) -> list[OcrComparison]:
    results = []
    for adapter in adapters:
        started = perf_counter()
        page = adapter.extract(image_path)
        elapsed = perf_counter() - started
        confidence = sum(b.confidence for b in page.blocks) / len(page.blocks) if page.blocks else 0.0
        results.append(OcrComparison(adapter.name, elapsed, ' '.join(b.text for b in page.blocks), confidence, len(page.blocks)))
    return results