from backend.ocr.models import OcrBlock


class TableCandidateDetector:
    def detect(self, blocks: list[OcrBlock]) -> list[OcrBlock]:
        candidates: list[OcrBlock] = []

        for block in blocks:
            text = block.text
            if "|" in text or text.count("\t") >= 2:
                candidates.append(block)

        return candidates
