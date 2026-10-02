from pathlib import Path

from backend.reconstruction.equation_renderer import EquationRenderer
from backend.reconstruction.image_renderer import ImageRenderer
from backend.reconstruction.models import RenderDocument
from backend.reconstruction.table_renderer import TableRenderer
from backend.reconstruction.text_fitter import TextFitter


class PdfRenderer:
    def __init__(
        self,
        text_fitter: TextFitter | None = None,
        font_path: str | None = None,
        font_name: str = "SCI_DOC_UNICODE",
        equation_renderer: EquationRenderer | None = None,
        table_renderer: TableRenderer | None = None,
        image_renderer: ImageRenderer | None = None,
    ) -> None:
        self.text_fitter = text_fitter or TextFitter()
        self.font_path = font_path
        self.font_name = font_name
        self.equation_renderer = equation_renderer or EquationRenderer()
        self.table_renderer = table_renderer or TableRenderer()
        self.image_renderer = image_renderer or ImageRenderer()

    def _register_font(self, pdfmetrics) -> str:
        if not self.font_path:
            return "Helvetica"

        font_file = Path(self.font_path)
        if not font_file.exists():
            raise FileNotFoundError(f"Configured reconstruction font not found: {font_file}")

        from reportlab.pdfbase.ttfonts import TTFont

        pdfmetrics.registerFont(TTFont(self.font_name, str(font_file)))
        return self.font_name

    def render(self, document: RenderDocument, output_path: str | Path) -> Path:
        try:
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfgen import canvas
        except ImportError as exc:
            raise RuntimeError("reportlab is required for PDF reconstruction") from exc

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        font_name = self._register_font(pdfmetrics)

        pdf = canvas.Canvas(str(output))

        for page in document.pages:
            pdf.setPageSize((page.width, page.height))

            for element in page.elements:
                if element.element_type == "table":
                    self.table_renderer.draw(pdf, element, page.height)
                    continue
                if element.element_type == "image":
                    self.image_renderer.draw(pdf, element, page.height)
                    continue
                if element.element_type == "equation":
                    self.equation_renderer.draw(pdf, element, page.height)
                    continue
                if not element.text:
                    continue

                fit = self.text_fitter.fit(
                    element.text,
                    box_width=element.width,
                    box_height=element.height,
                )
                if not fit.lines:
                    continue

                pdf.setFont(font_name, fit.font_size)
                y = page.height - element.y - fit.font_size

                for line in fit.lines:
                    pdf.drawString(element.x, y, line)
                    y -= fit.font_size * 1.25

            pdf.showPage()

        pdf.save()
        return output
