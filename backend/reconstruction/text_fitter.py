from dataclasses import dataclass


@dataclass(frozen=True)
class TextFit:
    font_size: float
    lines: list[str]
    fits: bool


class TextFitter:
    def fit(
        self,
        text: str,
        *,
        box_width: float,
        box_height: float,
        base_font_size: float = 12,
    ) -> TextFit:
        if not text:
            return TextFit(base_font_size, [], True)

        # Deterministic first-pass approximation. A production renderer will
        # measure actual font glyphs for the selected Hindi/Marathi font.
        chars_per_line = max(1, int(box_width / max(base_font_size * 0.55, 1)))
        lines = [
            text[index:index + chars_per_line]
            for index in range(0, len(text), chars_per_line)
        ]

        line_height = base_font_size * 1.25
        fits = len(lines) * line_height <= box_height

        font_size = base_font_size
        while not fits and font_size > 6:
            font_size -= 0.5
            chars_per_line = max(1, int(box_width / max(font_size * 0.55, 1)))
            lines = [
                text[index:index + chars_per_line]
                for index in range(0, len(text), chars_per_line)
            ]
            fits = len(lines) * font_size * 1.25 <= box_height

        return TextFit(font_size, lines, fits)
