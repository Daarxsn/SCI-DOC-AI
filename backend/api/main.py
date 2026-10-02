from fastapi import FastAPI
from backend.api.jobs import router as jobs_router
from backend.api.upload import router as upload_router

app = FastAPI(title="SCI-DOC AI", version="0.7.0", description="Enterprise scientific document intelligence, translation, validation, and reconstruction API.")
app.include_router(upload_router)
app.include_router(jobs_router)

@app.get("/health", tags=["system"])
def health():
    return {"status":"ok","service":"sci-doc-ai"}

@app.get("/ready", tags=["system"])
def ready():
    return {"status":"ready","service":"sci-doc-ai"}
