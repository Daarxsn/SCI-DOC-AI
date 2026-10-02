from fastapi import Request
from fastapi.responses import JSONResponse


def api_error(code: str, message: str, status_code: int, request: Request | None = None, details: dict | None = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "request_id": request.headers.get("X-Request-ID") if request else None,
                "details": details or {},
            }
        },
    )
