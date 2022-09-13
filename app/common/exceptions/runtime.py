##################################
# Base Runtime Exception
##################################

class DevonCustomException(RuntimeError):
    def __init__(self, detail: str = None):
        super().__init__()
        self.detail = detail


##################################
# Custom Runtime Exceptions
##################################

class UnexpectedStatusException(DevonCustomException):
    def __init__(self):
        super().__init__("Unexpected status found")


class ResourceNotFoundException(DevonCustomException):
    def __init__(self, detail="Resource not found"):
        super().__init__(detail)
