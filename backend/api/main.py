from fastapi import FastAPI
from backend.api.jobs import router as jobs_router
from backend.api.upload import router as upload_router
from backend.api.results import router as results_router
from backend.core.production import check_production_readiness

app = FastAPI(
    title="SCI-DOC AI",
    version="0.9.0",
    description="Enterprise scientific document intelligence, translation, validation, and reconstruction API.",
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
