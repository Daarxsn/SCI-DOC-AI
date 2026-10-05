# Frontend Phase 2 — Design System

## Objective
Establish the reusable visual system for SCI-DOC AI without changing the Phase 1 application architecture or backend contracts.

## Design tokens
The system defines centralized tokens for:
- semantic colors and surfaces
- typography scale and font families
- spacing
- border radii
- elevation/shadows
- layout dimensions
- focus treatment

Tokens live in `frontend/src/styles/tokens.css` and are consumed by the base stylesheet and UI primitives.

## Reusable primitives
F02 introduces:
- `Button`: primary, secondary, ghost, and danger variants; small/medium/large sizes
- `Card`: standard and interactive surfaces
- `Badge`: neutral, success, warning, danger, and info tones
- `TextField`: accessible label, input, and optional hint
- shared focus-visible behavior and responsive layout rules

## Product language
The visual direction is intentionally suited to scientific enterprise software:
- restrained navy/blue primary palette
- high-contrast readable text
- clean white surfaces
- subtle borders and elevation
- semantic status colors
- compact, information-dense controls
- responsive behavior for smaller screens

## F02 acceptance criteria
1. Design tokens are centralized and reusable.
2. Typography, spacing, color, radius, elevation, and focus states are defined.
3. Reusable button, card, badge, and text-field primitives exist.
4. Existing application shell consumes the new system.
5. Dashboard demonstrates the primitives without introducing mocked backend behavior.
6. Existing Phase 1 routes and API boundary remain intact.
7. Frontend production build passes in CI.

## Evidence boundary
Passing F02 proves the frontend design-system/build contract. It does not prove OCR, translation, scientific validation, reconstruction, authentication, or production deployment.
