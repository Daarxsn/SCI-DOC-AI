# Phase 4 — Production Reconstruction

UDR → render document → layout gate → source-page preservation → scientific renderers → deterministic PDF artifact.

## Production reconstruction contract

Phase 4 adds four guarantees:

1. **Source-page continuity** — processed page rasters can be passed directly from the E2E pipeline into reconstruction as page backgrounds.
2. **Layout gate** — reconstruction refuses export when an element has a page-boundary error unless the caller explicitly disables the gate.
3. **Artifact integrity** — every production export can be represented by a `ReconstructionArtifact` containing document ID, format, output path, byte size, SHA-256, page count, and layout-warning count.
4. **Deterministic mapping** — UDR elements retain their original geometry, translated text, source text, confidence and metadata when mapped into the render model.

## Source-page preservation

The E2E pipeline passes the processed page images into reconstruction. Text-like regions are covered and replaced while non-text artwork remains available from the source raster.

This preserves:

- page borders and lines;
- logos and watermarks;
- stamps and visual marks;
- diagrams/images that are not being replaced;
- original page geometry.

The current cover operation is still a white rectangle. It is a controlled baseline, not background-aware inpainting.

## Renderers

| Element | Current renderer |
|---|---|
| Text | PDF text fitting + optional Unicode raster path |
| Equation | LaTeX/MathML metadata with controlled Unicode fallback |
| Diagram / graph | Structured geometry primitives |
| Table | Deterministic PDF grid |
| Image | Positioned source asset |
| Source page | Optional processed raster background |

## Export safety

The reconstruction service validates layout before rendering. Boundary errors block export by default. The service also records a SHA-256 checksum and output metadata after a successful render.

## Phase 4 verification

The repository includes lightweight reconstruction tests covering:

- source-page path propagation;
- translated text mapping;
- layout overflow blocking;
- successful PDF creation;
- artifact checksum/size/page-count integrity.

CI is required to pass `scripts/verify_phase4.py` before Phase 4 is marked verified.

## Known next-level work

- background-aware inpainting/masking;
- font metrics and line breaking for production Hindi/Marathi fonts;
- high-fidelity equation rendering;
- trained scientific diagram reconstruction;
- pixel/structural fidelity benchmarking against real golden documents.
