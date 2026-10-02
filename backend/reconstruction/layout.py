from dataclasses import dataclass

from backend.reconstruction.models import RenderElement, RenderPage


@dataclass(frozen=True)
class LayoutIssue:
    severity: str
    element_id: str
    code: str
    message: str


class LayoutEngine:
    def validate_page(self, page: RenderPage, margin: float = 0) -> list[LayoutIssue]:
        issues: list[LayoutIssue] = []
        for element in page.elements:
            if element.x < margin or element.y < margin:
                issues.append(LayoutIssue("warning", element.element_id, "outside_margin", "Element starts inside the configured page margin."))
            if element.x + element.width > page.width - margin:
                issues.append(LayoutIssue("error", element.element_id, "horizontal_overflow", "Element extends beyond the page width."))
            if element.y + element.height > page.height - margin:
                issues.append(LayoutIssue("error", element.element_id, "vertical_overflow", "Element extends beyond the page height."))
        for index, first in enumerate(page.elements):
            for second in page.elements[index + 1:]:
                if self.overlaps(first, second):
                    issues.append(LayoutIssue("warning", second.element_id, "element_overlap", f"Element overlaps {first.element_id}."))
        return issues

    @staticmethod
    def overlaps(first: RenderElement, second: RenderElement) -> bool:
        return not (
            first.x + first.width <= second.x
            or second.x + second.width <= first.x
            or first.y + first.height <= second.y
            or second.y + second.height <= first.y
        )

    def sort_for_rendering(self, page: RenderPage) -> list[RenderElement]:
        return sorted(
            page.elements,
            key=lambda element: (
                int(element.metadata.get("z_index", 0)),
                element.y,
                element.x,
                element.element_id,
            ),
        )
