# Document Reconstruction

The reconstruction layer converts validated UDR elements back into a paginated document.

## Pipeline

UDR → RenderDocument → text fitting → PDF renderer.

## Coordinate System

UDR coordinates use a top-left origin. The PDF renderer converts the Y coordinate to ReportLab's bottom-left coordinate system.

## Current Baseline

The first renderer handles translated text regions and preserves page dimensions. Equations, diagrams, images, fonts, and background preservation are represented in the render contract but require specialized renderers.

## Safety

Reconstruction must not silently export a document that failed validation. The production orchestration layer will enforce the validation review gate before calling export.
