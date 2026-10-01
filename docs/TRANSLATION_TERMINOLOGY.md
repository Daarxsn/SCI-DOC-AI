# Scientific Translation and Terminology

Translation is element-aware rather than a single generic text operation.

## Policy

- Ordinary prose → translation adapter.
- Equations → specialized mathematics path + review.
- Diagrams/graphs → translate semantic labels while preserving structure.
- Images/page numbers → preserve.
- Low-confidence translation → human review.

## Terminology

The terminology registry stores controlled scientific vocabulary by target language and domain.

Each entry can specify:

- source term;
- approved target term;
- domain;
- whether the original must be preserved;
- provenance/notes.

## Adapter Strategy

The initial rule-based adapter is only a deterministic development adapter. A production NMT/LLM translation provider can implement the same adapter contract without changing UDR or validation layers.

The translation layer must never silently overwrite equations, scientific symbols, or specialized diagram structures.
