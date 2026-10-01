from backend.mathematics.service import MathematicsService


def test_unicode_math_is_normalized():
    equation = MathematicsService().process("F = m × a", confidence=0.95)

    assert equation.latex == r"F = m \times a"
    assert equation.validation_errors == []


def test_unbalanced_expression_is_flagged():
    equation = MathematicsService().process(r"\frac{1}{2", confidence=0.9)

    assert "unbalanced LaTeX braces" in equation.validation_errors


def test_symbol_metadata_is_created():
    equation = MathematicsService().process("E = mc²", confidence=0.8)

    assert any(symbol.symbol == "=" for symbol in equation.symbols)
