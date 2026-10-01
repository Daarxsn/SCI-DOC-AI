# M2 OCR-to-UDR Pipeline

M2 converts OCR output into a document-level UDR.

## Processing

1. OCR produces words, line blocks, coordinates, and confidence.
2. Structure analysis identifies questions, subquestions, tables, and equation candidates.
3. Elements receive UDR IDs, bounding boxes, provenance, and metadata.
4. Pages are assembled into a document-level UDR.
5. Specialized scientific modules can consume equation and diagram candidates later.

## Current Limitation

The structure analyzer is intentionally conservative and heuristic. It is not the final scientific layout model. A golden dataset will be used later to benchmark and replace weak heuristics with learned models where justified.
