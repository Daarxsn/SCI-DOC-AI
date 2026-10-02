from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

from backend.diagrams.models import DiagramDomain
from backend.diagrams.model_adapter import UltralyticsDiagramDetector
from backend.diagrams.service import DiagramService
from backend.diagrams.udr_adapter import DiagramUdrAdapter
from backend.mathematics.model_adapter import HybridEquationService
from backend.mathematics.udr_adapter import MathUdrAdapter
from backend.schemas.udr import ElementType, UdrDocument


class ScientificEnrichment:
    """Attach equation and diagram intelligence to an existing UDR."""

    def __init__(self, equation_provider="baseline", diagram_provider="baseline",
                 diagram_model="", device="auto"):
        self.equations = HybridEquationService(equation_provider, device)
        self.diagram_provider = diagram_provider
        self.diagram_detector = (
            UltralyticsDiagramDetector(diagram_model, device)
            if diagram_provider == "ultralytics" else None
        )
        self.diagram_service = DiagramService()
        self.math_adapter = MathUdrAdapter()
        self.diagram_adapter = DiagramUdrAdapter()

    def apply(self, document: UdrDocument, image_paths: list[str | Path]) -> UdrDocument:
        result = document.model_copy(deep=True)
        with TemporaryDirectory(prefix="sci-doc-enrich-") as temp_dir:
            for page_index, page in enumerate(result.pages):
                if page_index >= len(image_paths):
                    continue
                source = Path(image_paths[page_index])
                for element in page.elements:
                    if element.type == ElementType.EQUATION and element.source_text:
                        if self.equations.provider == "pix2tex":
                            crop = self._crop(source, element.bbox, Path(temp_dir) / f"{element.id}.png")
                            equation = self.equations.process_image(crop)
                        else:
                            equation = self.equations.process_text(element.source_text, element.confidence or 0.5)
                        self.math_adapter.enrich(element, equation)

                    if element.type in {ElementType.DIAGRAM, ElementType.GRAPH}:
                        domain = DiagramDomain(document.domain if document.domain in {x.value for x in DiagramDomain} else "general")
                        candidates = []
                        if self.diagram_detector:
                            candidates = self.diagram_detector.detect(source, domain)
                        labels = []
                        if element.bbox:
                            for other in page.elements:
                                if other is element or not other.source_text or not other.bbox:
                                    continue
                                if self._inside(other.bbox.x, other.bbox.y, element.bbox.x, element.bbox.y,
                                                element.bbox.width, element.bbox.height):
                                    labels.append({
                                        "text": other.source_text,
                                        "confidence": other.confidence or 0.5,
                                        "x": other.bbox.x, "y": other.bbox.y,
                                        "width": other.bbox.width, "height": other.bbox.height,
                                    })
                        diagram = self.diagram_service.analyze(
                            domain=domain, source_image_path=str(source),
                            label_candidates=labels, object_candidates=candidates,
                            confidence=min([x.get("confidence", 0.5) for x in candidates] or [element.confidence or 0.5]),
                        )
                        self.diagram_adapter.enrich(element, diagram)
        return result

    @staticmethod
    def _inside(x, y, bx, by, bw, bh):
        return bx <= x <= bx + bw and by <= y <= by + bh

    @staticmethod
    def _crop(source, bbox, output):
        if bbox is None:
            raise ValueError("Equation image recognition requires an element bounding box")
        with Image.open(source) as image:
            crop = image.crop((bbox.x, bbox.y, bbox.x + bbox.width, bbox.y + bbox.height))
            crop.save(output, format="PNG")
        return output
