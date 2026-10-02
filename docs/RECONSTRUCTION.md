# Document Reconstruction

The reconstruction layer converts validated UDR elements back into a paginated document.

## Pipeline

UDR → RenderDocument → scientific render plan → layout/composition → PDF.

## Render Contracts

Scientific content is not treated as ordinary prose.

| UDR element | Reconstruction adapter | Current baseline |
|---|---|---|
| text/question/heading | text fitter + PDF renderer | rendered |
| equation | equation renderer | LaTeX/MathML contract; specialized drawing pending |
| diagram/graph | diagram renderer | structured graph preserved; visual drawing pending |
| table | table renderer | normalized grid contract; visual drawing pending |
| image | image renderer | asset resolution contract |

## Why This Separation Exists

The UDR already carries scientific structure. Reconstruction should consume that structure rather than re-OCR the translated page or flatten scientific content into text.

This allows specialized renderers to be added independently:

- LaTeX/MathML equation renderer
- SVG/canvas diagram renderer
- grid/table renderer
- raster/vector image placement
- complex-script text shaping

## Fonts

Hindi/Marathi output requires a licensed Unicode/Devanagari-capable font supplied by deployment. Fonts are not bundled in this repository.

## Validation Gate

Reconstruction is an export stage, not a validation stage. The production orchestration layer must call the validation review gate before export and must not silently export a document that failed validation.

## Known Prototype Limitations

- ReportLab's basic text drawing is a baseline and is not yet a full complex-script shaping engine.
- Automatic font selection is not implemented.
- Equation, diagram, table, and image visual drawing adapters are not yet complete.
- Visual fidelity has not yet been benchmarked against real client documents.
