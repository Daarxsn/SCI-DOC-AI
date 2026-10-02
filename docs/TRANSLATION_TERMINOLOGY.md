# Translation Memory and Scientific Terminology

## Translation Memory

Translation memory stores approved source/target pairs scoped by:

- source language;
- target language;
- scientific domain;
- exact source text.

An exact memory hit is returned with confidence 1.0 and marked as originating from translation memory.

## Terminology Registry

Terminology entries are scoped by source language, target language, and domain. Longer terms are protected before shorter terms so overlapping terminology can be handled deterministically.

Protected terms are replaced after the translation adapter returns.

## Priority

The intended translation priority is:

1. approved translation-memory exact match;
2. protected scientific terminology;
3. configured translation model/adapter;
4. human review for low-confidence or unresolved content.

## Governance

Translation memory should contain approved translations only. Model-generated translations should not automatically become permanent memory entries without an approval workflow.

## Current limitation

The terminology protection path currently uses deterministic string replacement. Production deployment should add token-aware matching and morphology/context rules for inflected scientific language.
