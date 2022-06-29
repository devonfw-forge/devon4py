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
