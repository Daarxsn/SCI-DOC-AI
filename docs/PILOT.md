# Production Pilot — M9 Complete

M9 is the end-to-end integration boundary for SCI-DOC AI.

## Pipeline

Input document
→ ingestion/preprocessing
→ OCR/layout
→ UDR
→ translation adapter
→ M5 scientific validation
→ M6 human review when required
→ validation after review
→ reconstruction/export adapter
→ artifact/result API.

## Provider boundaries

M9 defines provider-neutral interfaces for:

- document storage;
- model/version registry;
- translation;
- export.

This allows the pilot to use cloud APIs, self-hosted models, or private/on-premise implementations without changing the orchestration contract.

## Pilot run state

Each run tracks:

- tenant;
- document;
- target language;
- domain;
- current stage;
- progress;
- review requirement;
- export decision;
- artifacts;
- error;
- model versions.

## Production deployment requirements

Before a real client deployment, configure:

1. persistent document/UDR storage;
2. durable queue and worker execution;
3. production OCR model;
4. production English→Hindi/Marathi translation model;
5. equation recognition/rendering model;
6. diagram/object/relationship models;
7. Unicode Devanagari font and shaping-capable renderer;
8. persistent review database;
9. object storage for PDF/PNG artifacts;
10. TLS, secret management, identity, audit logging, rate limiting;
11. golden benchmark dataset and acceptance thresholds.

## Pilot acceptance

A pilot should use a fixed document set and record:
- model versions;
- processing time;
- failure rate;
- review rate;
- validation-block rate;
- OCR metrics;
- translation metrics;
- equation integrity;
- diagram integrity;
- reconstruction fidelity;
- reviewer corrections.

Do not claim production accuracy until those measurements are collected.

## M9 acceptance criteria

- [x] End-to-end pilot run contract
- [x] Tenant-scoped run state
- [x] Provider abstraction
- [x] Model/version provenance
- [x] Translation → validation → export orchestration
- [x] Failure capture
- [x] Pilot status API
- [x] Integration tests
- [x] Production deployment checklist
