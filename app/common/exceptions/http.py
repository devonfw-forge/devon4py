from typing import Any, Optional, Dict

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
