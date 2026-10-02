from backend.reconstruction.equation_renderer import EquationRenderer


def test_latex_symbol_normalization():
    result = EquationRenderer()._latex_to_unicode(r"x \leq 2 \times \pi")
    assert result == "x ≤ 2 × π"


def test_unicode_renderer_is_safe_without_font():
    from backend.reconstruction.unicode_renderer import UnicodeTextRenderer
    assert UnicodeTextRenderer().available() is False
