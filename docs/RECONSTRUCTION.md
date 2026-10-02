# Document Reconstruction

UDR → RenderDocument → layout validation/composition → source-page baseline → scientific renderers → PDF.

## Source-Page Preservation

When a processed source-page raster is available, reconstruction can use it as the page background. Text-like regions are then covered and replaced with translated content while non-text page artwork remains visible.

This is intended to preserve:

- page borders and lines;
- logos and watermarks;
- stamps and visual marks;
- diagrams/images that are not being replaced;
- original page geometry.

The source page path is carried in render-page metadata as `source_page_path`.

## Important limitation

The current cover operation uses a white rectangle. This is a baseline strategy, not true background-aware inpainting. It works best for clean scanned question papers with light backgrounds.

Future work should add region-aware masking/inpainting and background classification so colored boxes, textured pages, and overlapping artwork are preserved.

## Renderers

| Element | Baseline |
|---|---|
| Text | PDF rendering + optional Unicode raster path |
| Equation | Controlled Unicode fallback |
| Diagram | Structured geometry when coordinates exist |
| Table | PDF grid |
| Image | Positioned asset |
| Source page | Optional raster background |

## Export safety

Validation and layout diagnostics must run before export. Reconstruction must not silently ignore critical validation failures.
