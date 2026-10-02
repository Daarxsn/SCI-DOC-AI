# Document Reconstruction

UDR → RenderDocument → scientific render plan → layout/composition → PDF.

## Current renderers

| Element | Baseline |
|---|---|
| Text | PDF rendering + optional Unicode raster path |
| Equation | Controlled Unicode fallback; dedicated typesetting pending |
| Diagram | Structured geometry when coordinates exist |
| Table | PDF grid |
| Image | Positioned asset |

## Indic text

With a licensed Unicode/Devanagari-capable TrueType font configured, text can be rasterized through Pillow before placement into the PDF. This provides a practical shaping path for Hindi/Marathi output without claiming that basic ReportLab text APIs perform complex-script shaping.

Fonts are not bundled in the repository.

## Equations

LaTeX/MathML metadata is preserved. A small controlled LaTeX-symbol normalization provides a deterministic fallback. Full LaTeX/MathML typesetting remains a separate adapter.

## Export safety

The validation review gate must run before export. Reconstruction itself does not override validation failures.

## Known limitations

- Full LaTeX/MathML typesetting is pending.
- Diagram semantics and domain-specific shapes are only partially reconstructed.
- Visual fidelity has not yet been benchmarked against real client documents.
