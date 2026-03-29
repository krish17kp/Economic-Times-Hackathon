"""
Custom exception classes.
Location: backend/app/core/exceptions.py
"""


class AgroAIException(Exception):
    """Base exception for all AgroAI errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(AgroAIException):
    def __init__(self, resource: str, identifier: str = ""):
        msg = f"{resource} not found"
        if identifier:
            msg = f"{resource} '{identifier}' not found"
        super().__init__(message=msg, status_code=404)


class InsufficientDataError(AgroAIException):
    def __init__(self, detail: str):
        super().__init__(message=f"Insufficient data: {detail}", status_code=422)


class LocationRequiredError(AgroAIException):
    def __init__(self):
        super().__init__(
            message="Location required. Provide latitude/longitude or pincode.",
            status_code=400,
        )
