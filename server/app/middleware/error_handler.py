from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def register_error_handler(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def handle_exception(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=500, content={"detail": "internal_server_error"})
