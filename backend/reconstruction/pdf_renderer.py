from pathlib import Path

from backend.reconstruction.models import RenderDocument
from backend.reconstruction.text_fitter import TextFitter


class PdfRenderer:
    def __init__(self, text_fitter: TextFitter | None = None) -> None:
        self.text_fitter = text_fitter or TextFitter()

    def render(self, document: RenderDocument, output_path: str | Path) -> Path:
        try:
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfgen import canvas
        except ImportError as exc:
            raise RuntimeError("reportlab is required for PDF reconstruction") from exc

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

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

                font_size = fit.font_size
                pdf.setFont("Helvetica", font_size)

                # PDF coordinates originate at the bottom-left while UDR
                # coordinates originate at the top-left.
                y = page.height - element.y - font_size

                for line in fit.lines:
                    pdf.drawString(element.x, y, line)
                    y -= font_size * 1.25

            pdf.showPage()

        pdf.save()
        return output
