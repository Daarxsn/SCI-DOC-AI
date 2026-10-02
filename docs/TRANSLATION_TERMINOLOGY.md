# Translation Intelligence — M4 Complete

## Document-level orchestration
The UDR is translated without flattening scientific structure. Prose/questions are translated, equations/images/graphs are preserved, and diagram labels are translated independently while coordinates and relationships remain intact.

## Translation memory
Approved source/target pairs are stored by source language, target language, scientific domain, and exact source text. Model output is not automatically promoted to permanent memory.

## Scientific terminology
Terminology is scoped by language pair and domain. Longer terms are protected before shorter terms.

## Human review
Low-confidence units enter a review queue. Reviewers can accept, edit, or reject translations. Only approved non-empty translations can be promoted to Translation Memory.

## Governance
Approval activity can be recorded with actor, timestamp, language pair, domain, source, target, action, and reason.

## Pipeline result
The translation pipeline returns the translated UDR plus explicit review-required and review-count state.

## Adapter boundary
Translation models remain pluggable behind TranslationAdapter. The development rule-based adapter is intentionally low-confidence and is not a production translation claim.

## M4 acceptance criteria
- [x] Translation memory
- [x] Scientific terminology
- [x] Domain/language scoping
- [x] Document translation orchestration
- [x] Diagram-label translation
- [x] Review queue
- [x] Approval path
- [x] Governance/audit contract
- [x] Pipeline-level review status
- [x] Pluggable translation adapter
