# Document Reconstruction

The reconstruction layer converts validated UDR elements back into a paginated document.

## Pipeline

UDR → RenderDocument → scientific render plan → layout/composition → PDF.

## Render Contracts

| UDR element | Reconstruction adapter | Current baseline |
|---|---|---|
| text/question/heading | text fitter + PDF renderer | rendered |
| equation | equation renderer | text fallback; specialized typesetting pending |
| diagram/graph | diagram renderer | structured geometry rendered when coordinates exist |
| table | table renderer | PDF grid rendered |
| image | image renderer | positioned asset rendered |

## Diagram Reconstruction

The baseline diagram renderer consumes structured UDR metadata:

- object bounding boxes;
- label coordinates;
- relationship source/target points.

It draws those primitives relative to the diagram bounding box. If detector metadata has no geometry, the renderer does not invent positions and reports an adapter-required state in its render plan.

This is deliberately conservative: reconstructed scientific diagrams must be traceable to detected structure.

## Equations

Equations currently use a text fallback. LaTeX and MathML are preserved in the render contract so a specialized typesetting adapter can be plugged in without changing UDR.

## Fonts

Hindi/Marathi output requires a licensed Unicode/Devanagari-capable font supplied by deployment. Fonts are not bundled in this repository.

## Validation Gate

Reconstruction is an export stage, not a validation stage. The production orchestration layer must call the validation review gate before export and must not silently export a document that failed validation.

## Known Prototype Limitations

- ReportLab's basic text drawing is not a complete complex-script shaping engine.
- Equation visual typesetting is not yet implemented.
- Diagram semantics such as arrows, symbols, domain-specific shapes, and connector routing are not yet fully reconstructed.
- Visual fidelity has not yet been benchmarked against real client documents.
