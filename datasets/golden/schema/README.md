# Annotation schema

Every annotated benchmark case can record:

- **text** — OCR ground truth and translated reference text;
- **layout** — element bounding boxes and reading order;
- **equation** — normalized LaTeX/MathML reference;
- **diagram** — objects, labels and relationships;
- **table** — rows, columns and cell content;
- **document** — page/document metadata.

Annotations must be tied to a page and stable element identifier where possible.

Scientific annotations should preserve the original equation/diagram representation rather than relying only on rendered text.
