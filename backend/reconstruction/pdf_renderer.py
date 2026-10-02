from pathlib import Path

from backend.reconstruction.models import RenderDocument
from backend.reconstruction.text_fitter import TextFitter


class PdfRenderer:
    def __init__(
        self,
        text_fitter: TextFitter | None = None,
        font_path: str | None = None,
        font_name: str = "SCI_DOC_UNICODE",
    ) -> None:
        self.text_fitter = text_fitter or TextFitter()
        self.font_path = font_path
        self.font_name = font_name

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

                # UDR coordinates use a top-left origin; PDF uses bottom-left.
                y = page.height - element.y - fit.font_size

                for line in fit.lines:
                    pdf.drawString(element.x, y, line)
                    y -= fit.font_size * 1.25

            pdf.showPage()

        pdf.save()
        return output
