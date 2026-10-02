from backend.reconstruction.models import RenderElement


class DiagramRenderer:
    """Render structured diagram metadata into deterministic PDF primitives."""

    def render(self, element: RenderElement) -> dict:
        objects = element.metadata.get("objects", [])
        labels = element.metadata.get("labels", [])
        relationships = element.metadata.get("relationships", [])

        return {
            "element_id": element.element_id,
            "domain": element.metadata.get("domain", "general"),
            "objects": objects,
            "labels": labels,
            "relationships": relationships,
            "bbox": {
                "x": element.x,
                "y": element.y,
                "width": element.width,
                "height": element.height,
            },
            "render_status": "ready" if any(
                self._has_geometry(item) for item in [*objects, *labels, *relationships]
            ) else "adapter_required",
        }

    @staticmethod
    def _has_geometry(item: dict) -> bool:
        return any(key in item for key in ("x", "y", "bbox", "source_bbox", "target_bbox"))

    @staticmethod
    def _point(value):
        if isinstance(value, dict) and "x" in value and "y" in value:
            return float(value["x"]), float(value["y"])
        if isinstance(value, (list, tuple)) and len(value) >= 2:
            return float(value[0]), float(value[1])
        return None

    @staticmethod
    def _bbox(item):
        bbox = item.get("bbox") if isinstance(item, dict) else None
        if isinstance(bbox, dict) and all(k in bbox for k in ("x", "y", "width", "height")):
            return (
                float(bbox["x"]),
                float(bbox["y"]),
                float(bbox["width"]),
                float(bbox["height"]),
            )
        if isinstance(item, dict) and all(k in item for k in ("x", "y")):
            return (
                float(item["x"]),
                float(item.get("width", 20)),
                float(item["y"]),
                float(item.get("height", 20)),
            )
        return None

    def draw(self, pdf, element: RenderElement, page_height: float) -> None:
        objects = element.metadata.get("objects", [])
        labels = element.metadata.get("labels", [])
        relationships = element.metadata.get("relationships", [])

        # Diagram-local coordinates are expected to be relative to the
        # diagram's bounding box when local coordinates are supplied.
        origin_x, origin_y = element.x, page_height - element.y - element.height

        pdf.setLineWidth(0.8)

        for obj in objects:
            bbox = self._bbox(obj)
            if not bbox:
                continue

            x, y, width, height = bbox
            pdf.rect(origin_x + x, origin_y + element.height - y - height, width, height)

        for relation in relationships:
            source = self._point(relation.get("source_point"))
            target = self._point(relation.get("target_point"))

            if source and target:
                sx, sy = source
                tx, ty = target
                pdf.line(
                    origin_x + sx,
                    origin_y + element.height - sy,
                    origin_x + tx,
                    origin_y + element.height - ty,
                )

        for label in labels:
            point = self._point(label)
            if not point:
                bbox = self._bbox(label)
                if bbox:
                    point = (bbox[0], bbox[1])
            if not point:
                continue

            x, y = point
            text = label.get("text")
            if text:
                pdf.setFont("Helvetica", 8)
                pdf.drawString(
                    origin_x + x,
                    origin_y + element.height - y,
                    str(text),
                )
