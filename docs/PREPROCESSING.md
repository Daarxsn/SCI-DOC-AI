# Document Preprocessing

Preprocessing sits between ingestion and document understanding.

## Goals

- Normalize orientation metadata.
- Produce OCR-friendly grayscale images.
- Normalize contrast.
- Render PDF pages at a controlled DPI.
- Preserve page numbering and source provenance.
- Produce deterministic page artifacts.

## Default

The initial pipeline targets **300 DPI** and PNG output for processed pages.

## Pipeline

PDF/JPG/PNG → orientation normalization → color normalization → grayscale → autocontrast → page artifact.

Preprocessing deliberately does not perform OCR or semantic interpretation. Those responsibilities belong to later pipeline stages.
