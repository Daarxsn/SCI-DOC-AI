# SCI-DOC AI Golden Dataset

This directory contains the versioned benchmark contract for scientific document evaluation.

## Asset policy

Do not commit confidential client documents or copyrighted examination papers unless redistribution rights are confirmed.

The repository stores:
- dataset manifests;
- annotation schemas;
- non-sensitive structural fixtures;
- benchmark metadata.

Real document assets may be mounted from controlled storage and referenced by relative paths.

## Coverage target

| Domain | Source | Targets |
|---|---|---|
| Mathematics | English | Hindi, Marathi |
| Physics | English | Hindi, Marathi |
| Biology | English | Hindi, Marathi |

The benchmark should contain clean scans, noisy scans, skewed pages, equations, tables, scientific diagrams, labels, and mixed-content pages.

## Case naming

Use:

`<domain>-<target>-<number>`

Example: `physics-hi-001`.
