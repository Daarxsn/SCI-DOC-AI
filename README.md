# SCI-DOC AI

> Multimodal scientific document intelligence for scanned educational and examination documents.

SCI-DOC AI is an enterprise-oriented platform for turning difficult scientific documents into structured, reviewable, validated, and reconstructable digital outputs. The current product direction focuses on scanned educational/examination material in **Mathematics, Physics, and Biology**, with an initial translation scope of **English → Hindi / Marathi**.

The platform is designed around a strict principle:

> **Never present an inferred capability as a verified capability.**

The repository therefore separates implementation from evidence. A phase is considered locked only when its defined verification evidence passes.

---

## Product Vision

SCI-DOC AI is designed to combine:

- Document ingestion and OCR
- Scientific document understanding
- Equation recognition
- Diagram understanding
- Terminology control
- Translation memory
- Semantic validation
- Mathematical validation
- Diagram-aware validation
- Document reconstruction
- Human review
- API-first enterprise integration
- Security and tenant-aware controls
- Model/runtime registry and operational readiness

The initial workflow is intentionally constrained to the capabilities actually exposed by the current backend contracts. Scientific model quality is not claimed merely because a UI component exists.

---

## Current Architecture

```text
                    ┌──────────────────────────────┐
                    │        Enterprise Users      │
                    │ Reviewer / Operator / API    │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │ React + TypeScript Frontend  │
                    │ Vite / Router / Typed API    │
                    └──────────────┬───────────────┘
                                   │ HTTP
                                   ▼
                    ┌──────────────────────────────┐
                    │        FastAPI Backend       │
                    │                              │
                    │ Health / Ready / Runtime     │
                    │ Document Upload              │
                    │ Job Lifecycle                │
                    │ Result Retrieval             │
                    └──────────────┬───────────────┘
                                   │
                 ┌─────────────────┼─────────────────┐
                 ▼                 ▼                 ▼
          Document Intake      Processing        Results
          / metadata           jobs/status       artifacts
```

The backend is the source of truth for API behavior. The frontend consumes typed contracts and does not fabricate missing identifiers or scientific outputs.

---

## Repository Structure

```text
SCI-DOC-AI/
├── backend/
│   ├── api/
│   │   ├── main.py
│   │   ├── upload.py
│   │   ├── jobs.py
│   │   └── results.py
│   └── ...
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── styles/
│   ├── package.json
│   └── .env.example
├── datasets/
│   └── golden/
├── docs/
├── scripts/
├── tests/
├── Dockerfile
├── Dockerfile.ml
├── docker-compose.yml
├── docker-compose.staging.yml
├── docker-compose.production.yml
├── pytest.ini
└── README.md
```

---

## Frontend

The frontend is a React 19 + TypeScript + Vite application.

### Routes

| Route | Purpose |
|---|---|
| `/dashboard` | Platform health, readiness and runtime overview |
| `/documents` | Document intake/upload |
| `/documents/:documentId` | Results and artifact workspace |
| `/jobs` | Create and monitor processing jobs |
| `/jobs/:jobId` | Deep-linkable job monitoring |
| `/settings` | Frontend settings/configuration surface |

### Frontend workflow

```text
Document Intake
     │
     ▼
Backend Document Contract
     │
     ▼
Job Creation
     │
     ▼
Job Monitoring
     │
     ▼
Document Results
     │
     ▼
Artifact Provenance & Review
```

The current upload API returns document metadata/pages but does not return a document ID. The UI therefore does not invent one. Job creation currently requires a backend-valid document ID supplied through the existing contract.

---

## Backend API

### System endpoints

#### Health

```http
GET /health
```

Basic service health.

#### Readiness

```http
GET /ready
```

Returns readiness status, individual checks, and errors.

#### Runtime

```http
GET /runtime
```

Returns runtime/model-registry status exposed by the backend.

### Document upload

```http
POST /api/v1/documents/upload
```

Multipart document upload.

The current response includes:

- status
- filename
- MIME type
- size
- page metadata

### Jobs

```http
POST /v1/jobs
GET  /v1/jobs/{job_id}
```

Job creation and lifecycle monitoring are protected by the backend's API-key/scope boundary.

The frontend polls active jobs and handles terminal states such as `completed` and `failed`.

### Results

```http
GET /v1/documents/{document_id}/results
```

Returns:

- document ID
- result status
- artifact metadata

Current artifact metadata includes:

- tenant ID
- document ID
- artifact ID
- format
- path
- size
- optional checksum

The frontend deliberately treats these artifacts as metadata unless the backend exposes additional content semantics.

---

## Local Development

### Requirements

- Node.js 22+ recommended for frontend CI parity
- npm
- Python 3.12 for backend/container development
- Docker Desktop if using the repository's Docker workflow

### Frontend

From the repository root:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

### Frontend environment

Copy the example configuration:

```bash
cp frontend/.env.example frontend/.env
```

Example:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_API_KEY=
```

Do not commit real API keys.

### Frontend production build

```bash
cd frontend
npm install
npm run build
npm run verify:release
```

The release verification checks that the production build contains the expected application entrypoint.

---

## Backend with Docker

The repository includes a Docker-based API deployment path.

Verify Docker first:

```bash
docker --version
docker compose version
```

Then:

```bash
docker compose up --build
```

The API is exposed on:

```text
http://localhost:8000
```

Basic verification:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl http://localhost:8000/runtime
```

If Docker is not installed, install Docker Desktop before using the compose workflow.

---

## Security Model

The repository is designed with explicit security boundaries.

### API keys

Protected job/results operations use the backend API-key mechanism. The frontend can send:

```http
X-API-Key: <key>
```

through `VITE_API_KEY`.

### Secrets

Never commit:

- API keys
- cloud credentials
- production passwords
- signing secrets
- private certificates
- real customer documents

Use environment variables or the appropriate deployment secret store.

### Data handling

Scientific and examination documents can contain sensitive educational information. Production deployments should enforce appropriate:

- authentication
- authorization
- tenant isolation
- encryption
- retention controls
- audit logging
- secure storage
- network controls

A passing frontend build does not itself prove these controls are correctly deployed.

---

## Evidence-First Engineering

SCI-DOC AI uses an explicit implementation/evidence distinction.

### Implemented

Code exists and passes its defined local/static checks.

### Verified

The relevant automated verification has passed.

### Locked

The phase's acceptance criteria and CI evidence are GREEN and the phase is safe to treat as complete within its defined scope.

### Not implied

A green build does **not** automatically prove:

- OCR accuracy
- translation accuracy
- equation recognition accuracy
- diagram understanding accuracy
- mathematical correctness
- reconstruction fidelity
- real customer acceptance
- production infrastructure readiness

Those require domain-specific evaluation and real evidence.

---

## Frontend Phase Roadmap

| Phase | Focus | Current state |
|---|---|---|
| F01 | Frontend architecture | Implemented |
| F02 | Design system | Implemented |
| F03 | API integration/runtime state | Implemented |
| F04 | Document intake | Implemented |
| F05 | Job lifecycle | Implemented |
| F06 | Results workspace | Implemented |
| F07 | Workflow handoff | Implemented |
| F08 | Artifact provenance/review | Implemented |
| F09 | Artifact review controls | Implemented; CI verification pending/failing fix |
| F10 | Production release readiness | Implemented; CI evidence required |
| F11 | Operational diagnostics | Implemented; CI evidence required |
| F12 | Security hardening | Implemented; CI evidence required |
| F13 | Runtime & model readiness | Implemented; CI evidence required |
| F14 | Document → job handoff | Implemented; CI evidence required |
| F15 | Results & artifact validation | Implemented; CI evidence required |
| F16 | Accessibility & UX hardening | Implemented; CI evidence required |
| F17 | Local E2E smoke verification | Implemented; CI evidence required |

Phase status must be interpreted together with CI evidence. A phase is not called locked merely because its source files exist.

---

## CI

GitHub Actions validates phase-specific frontend changes.

Frontend CI follows the same fundamental release check:

```bash
npm install
npm run build
```

Phase-specific workflows are stored under:

```text
.github/workflows/
```

The repository also contains broader backend verification workflows.

---

## Scientific Quality Roadmap

The product vision extends beyond the current API shell. Future scientific evaluation should be evidence-driven against controlled datasets.

Recommended evaluation dimensions include:

| Capability | Example evidence |
|---|---|
| OCR | Character/word accuracy |
| Mathematical extraction | Equation recognition accuracy |
| Translation | Human/automatic translation evaluation |
| Terminology | Domain terminology consistency |
| Diagrams | Structure/label recognition |
| Semantic validation | Error detection rate |
| Reconstruction | Layout and visual fidelity |
| End-to-end | Golden-set task success |

The golden dataset should remain versioned and reproducible.

---

## Enterprise Deployment Direction

The intended deployment model is API-first and suitable for enterprise integration.

Target deployment layers include:

```text
Enterprise Client
      │
      ▼
API Gateway / Authentication
      │
      ▼
SCI-DOC AI API
      │
      ├── Document Processing
      ├── Scientific Understanding
      ├── Translation
      ├── Validation
      ├── Reconstruction
      └── Review / Audit
```

Production deployment must be validated separately from repository-level build checks.

---

## Development Principles

1. **Backend contracts are authoritative.**
2. **No fabricated IDs or result semantics.**
3. **Typed interfaces at frontend/API boundaries.**
4. **Evidence before lock.**
5. **Scientific claims require scientific evaluation.**
6. **Security controls must be explicit.**
7. **Production readiness must be demonstrated, not assumed.**
8. **Changes should remain reviewable and phase-scoped.**

---

## Status

SCI-DOC AI is an actively developed enterprise prototype moving through a controlled frontend/backend verification roadmap.

The repository should be treated as a **development/release-candidate codebase**, not as proof that every envisioned scientific capability is production-validated.

For the exact current state, use the GitHub Actions results and phase documentation in `docs/`.
