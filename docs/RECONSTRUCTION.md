# Document Reconstruction

UDR → RenderDocument → layout validation/composition → scientific renderers → PDF.

## Layout Safety

The reconstruction layout engine checks every page for horizontal/vertical overflow, configured margin violations, element collisions, and deterministic z-order.

Overlaps are warnings because some documents intentionally layer annotations or images. Page overflow is an error because content outside the page cannot be safely reconstructed.

## Renderers

| Element | Baseline |
|---|---|
| Text | PDF rendering + optional Unicode raster path |
| Equation | Controlled Unicode fallback; dedicated typesetting pending |
| Diagram | Structured geometry when coordinates exist |
| Table | PDF grid |
| Image | Positioned asset |

## Export

Layout diagnostics are exposed separately from rendering so the orchestration/API layer can require human review when reconstruction introduces a collision or overflow.

The validation review gate must still run before export.

Automatic collision resolution is intentionally not implemented yet; diagnostics are safer than silently moving scientific content.
