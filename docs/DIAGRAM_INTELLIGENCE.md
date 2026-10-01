# Diagram Intelligence

SCI-DOC AI represents diagrams as structured objects instead of treating them as unstructured images.

## Representation

A diagram contains:

- domain;
- labels;
- detected objects;
- relationships;
- confidence;
- source image provenance.

## Initial Domains

- Physics
- Biology
- General scientific diagrams

## Architecture

Diagram region → label extraction → object detection → relationship graph → UDR diagram element.

The current implementation is a baseline contract. Production recognition will use a specialized vision model while preserving the same downstream representation.

## Translation Principle

Diagram labels should be translated as independent semantic elements while the original label, coordinates, and relationship graph remain available for reconstruction.
