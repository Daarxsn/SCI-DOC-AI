from backend.reconstruction.diagram_renderer import DiagramRenderer
from backend.reconstruction.equation_renderer import EquationRenderer
from backend.reconstruction.image_renderer import ImageRenderer
from backend.reconstruction.models import RenderDocument
from backend.reconstruction.table_renderer import TableRenderer


class ReconstructionComposer:
    def __init__(
        self,
        equation_renderer: EquationRenderer | None = None,
        diagram_renderer: DiagramRenderer | None = None,
        table_renderer: TableRenderer | None = None,
        image_renderer: ImageRenderer | None = None,
    ) -> None:
        self.equation_renderer = equation_renderer or EquationRenderer()
        self.diagram_renderer = diagram_renderer or DiagramRenderer()
        self.table_renderer = table_renderer or TableRenderer()
        self.image_renderer = image_renderer or ImageRenderer()

    def plan(self, document: RenderDocument) -> list[dict]:
        plan: list[dict] = []

        for page in document.pages:
            for element in page.elements:
                if element.element_type == "equation":
                    result = self.equation_renderer.render(element)
                elif element.element_type in {"diagram", "graph"}:
                    result = self.diagram_renderer.render(element)
                elif element.element_type == "table":
                    result = self.table_renderer.render(element)
                elif element.element_type == "image":
                    result = self.image_renderer.render(element)
                else:
                    result = {
                        "element_id": element.element_id,
                        "render_status": "text",
                    }

                result["page_number"] = page.page_number
                plan.append(result)

        return plan
