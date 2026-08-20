class IncidenTixError(Exception):
    def __init__(
        self,
        message: str,
        *,
        status_code: int = 500,
        code: str = "internal_error",
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code


class NotFoundError(IncidenTixError):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, status_code=404, code="not_found")


class ValidationAppError(IncidenTixError):
    def __init__(self, message: str = "Invalid request") -> None:
        super().__init__(message, status_code=400, code="validation_error")
