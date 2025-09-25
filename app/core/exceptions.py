class AnalyticsServiceException(Exception):
    """Base class for all analytics service exceptions"""
    def __init__(self, message: str, code: str = "500"):
        self.message = message
        self.code = code
        super().__init__(message)

class DatabaseConnectionException(AnalyticsServiceException):
    """Database connection error"""
    def __init__(self, message: str = "Database connection error"):
        super().__init__(message, "500")

class ValidationException(AnalyticsServiceException):
    """Data validation error"""
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, "400")