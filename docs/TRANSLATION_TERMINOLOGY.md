# Translation Memory and Scientific Terminology

## Document-Level Orchestration

DocumentTranslationService walks the UDR without flattening it. Prose and question elements are translated; equations, images, and graphs are preserved; diagram labels are translated independently while coordinates and relationships remain untouched. Translation IDs, confidence, and status are written into UDR metadata.

## Translation Memory

Translation memory stores approved source/target pairs scoped by source language, target language, scientific domain, and exact source text.

## Terminology Registry

Terminology entries are scoped by language pair and domain. Longer terms are protected before shorter terms.

## Priority

1. approved translation-memory exact match;
2. protected scientific terminology;
3. configured translation adapter;
4. human review for low-confidence or unresolved content.

Only approved translations should enter permanent Translation Memory.

## Current limitation

Terminology protection is deterministic string replacement. Production should add token-aware matching and morphology/context rules.
