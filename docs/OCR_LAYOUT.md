# OCR and Layout Understanding

M2 introduces an adapter-based OCR layer.

## Current Baseline

Tesseract is the first OCR adapter. It returns word-level coordinates and confidence values, which are grouped into line blocks and mapped into UDR elements.

## Layout Baseline

The initial classifier recognizes equations using mathematical/operator patterns, multiple-choice option markers, short uppercase headings, and paragraphs as the default.

This is deliberately a baseline. A production layout model will replace or augment these heuristics after the golden dataset is established.

## Provenance

Every OCR-derived UDR element records the OCR engine and version so downstream validation and model-regression analysis can trace its origin.
