from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import IncidenTixError
from app.schemas.error import ErrorResponse


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(IncidenTixError)
    async def handle_app_error(
        _request: Request, exc: IncidenTixError
    ) -> JSONResponse:
        payload = ErrorResponse(code=exc.code, message=exc.message)
        return JSONResponse(
            status_code=exc.status_code,
            content=payload.model_dump(),
        )
