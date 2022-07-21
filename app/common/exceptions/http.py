from typing import Any, Optional, Dict, List

from fastapi import HTTPException


##################################
# Base HTTP Exception
##################################


class DevonHttpException(HTTPException):
    def __init__(self, status_code: int, detail: str = None, headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


##################################
# Custom HTTP Exceptions
##################################

class NotFoundException(DevonHttpException):
    def __init__(self, detail: str = "Not found", headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=404, detail=detail, headers=headers)


class DevonHttpExceptionWithCustomHeader(DevonHttpException):
    def __init__(self):
        super().__init__(status_code=403, detail="Custom Header Exception", headers={"X-Error": "There goes my error"})


class BearerAuthenticationNeededException(DevonHttpException):
    def __init__(self, detail: str = "Bearer authentication is needed"):
        super().__init__(status_code=401, detail=detail,
                         headers={'WWW-Authenticate': 'Bearer realm="auth_required"'})


class InvalidFirebaseAuthenticationException(DevonHttpException):
    def __init__(self, error: Exception = None):
        super().__init__(status_code=401, detail=f"Invalid authentication from Firebase. {error}",
                         headers={'WWW-Authenticate': 'Bearer error="invalid_token"'})


class UnauthorizedException(DevonHttpException):
    def __init__(self, roles: List[str] = None):
        super().__init__(status_code=401, detail=f"Unauthorized user. Required roles {roles}")
