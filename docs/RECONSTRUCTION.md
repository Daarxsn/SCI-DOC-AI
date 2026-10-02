# Document Reconstruction

The reconstruction layer converts validated UDR elements back into a paginated document.

## Pipeline

UDR → RenderDocument → text fitting → PDF renderer.

## Coordinate System

UDR coordinates use a top-left origin. The PDF renderer converts the Y coordinate to ReportLab's bottom-left coordinate system.

## Current Baseline

The renderer currently provides a deterministic text-first PDF baseline:

- preserves UDR page dimensions;
- uses translated `target_text` when available;
- preserves element coordinates and bounding boxes;
- fits long text into its source bounding box;
- supports an externally supplied TrueType/Unicode font;
- does not bundle third-party fonts.

Configure a licensed Devanagari-capable font in the deployment environment for Hindi/Marathi output. The font path is passed to `PdfRenderer(font_path=...)`.

## Scientific Elements

Equations, diagrams, graphs, tables, and images remain typed UDR elements. Their dedicated renderers are intentionally separate from the text renderer so scientific content can be reconstructed without flattening it into ordinary prose.

## Validation Gate

Reconstruction is an export stage, not a validation stage. The production orchestration layer must call the validation review gate before export and must not silently export a document that failed validation.

## Known Prototype Limitations

- ReportLab's basic text drawing is a baseline and is not yet a full complex-script shaping engine.
- Automatic font selection is not implemented.
- Equation, diagram, table, and image rendering adapters are not yet complete.
- Visual fidelity has not yet been benchmarked against real client documents.

These limitations are explicit so the prototype does not claim production-grade reconstruction prematurely.
