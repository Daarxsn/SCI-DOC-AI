import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.jobs import router as jobs_router
from backend.api.upload import router as upload_router
from backend.api.results import router as results_router
from backend.core.production import check_production_readiness
from backend.core.model_registry import runtime_status

app = FastAPI(
    title="SCI-DOC AI",
    version="1.0.0",
    description="Enterprise scientific document intelligence, translation, validation, and reconstruction API.",
)

cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "SCI_DOC_CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key"],
)

app.include_router(upload_router)
app.include_router(jobs_router)
app.include_router(results_router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "service": "sci-doc-ai"}


@app.get("/ready", tags=["system"])
def ready():
    readiness = check_production_readiness()
    return {
        "status": "ready" if readiness.ready else "not_ready",
        "service": "sci-doc-ai",
        "checks": readiness.checks,
        "errors": readiness.errors,
    }


@app.get("/runtime", tags=["system"])
def runtime():
    return {"service": "sci-doc-ai", **runtime_status()}
