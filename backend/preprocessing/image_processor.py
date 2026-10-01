from pathlib import Path

from backend.preprocessing.models import ImageMode, PageArtifact


class ImagePreprocessor:
    def __init__(self, target_dpi: int = 300) -> None:
        self.target_dpi = target_dpi

    def process(
        self,
        *,
        source_path: str | Path,
        output_path: str | Path,
        page_number: int = 1,
    ) -> PageArtifact:
        try:
            from PIL import Image, ImageOps
        except ImportError as exc:
            raise RuntimeError("Pillow is required for preprocessing") from exc

        source = Path(source_path)
        output = Path(output_path)

        with Image.open(source) as image:
            steps: list[str] = []

            image = ImageOps.exif_transpose(image)
            steps.append("exif_orientation")

            if image.mode not in ("RGB", "L"):
                image = image.convert("RGB")
                steps.append("color_normalization")

            grayscale = ImageOps.grayscale(image)
            grayscale = ImageOps.autocontrast(grayscale)
            steps.extend(["grayscale", "autocontrast"])

            output.parent.mkdir(parents=True, exist_ok=True)
            grayscale.save(output, format="PNG", dpi=(self.target_dpi, self.target_dpi))

            width, height = grayscale.size

        return PageArtifact(
            page_number=page_number,
            source_path=str(source),
            processed_path=str(output),
            width=width,
            height=height,
            rotation_degrees=0,
            image_mode=ImageMode.GRAYSCALE,
            dpi=self.target_dpi,
            preprocessing_steps=steps,
        )
