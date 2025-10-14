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

class MusicalMistakesNotFoundException(AnalyticsServiceException):
    """Musical mistakes not found error"""
    def __init__(self, message: str = "Musical mistakes not found"):
        super().__init__(message, "404")

class PosturalMistakesNotFoundException(AnalyticsServiceException):
    """Postural mistakes not found error"""
    def __init__(self, message: str = "Postural mistakes not found"):
        super().__init__(message, "404")

class TopScalesNotFoundException(AnalyticsServiceException):
    """Top scales not found error"""
    def __init__(self, message: str = "Top scales not found"):
        super().__init__(message, "404")

class WeeklyNotesNotFoundException(AnalyticsServiceException):
    """Weekly notes not found error"""
    def __init__(self, message: str = "Weekly notes not found"):
        super().__init__(message, "404")

class WeeklyTimePostureNotFoundException(AnalyticsServiceException):
    """Weekly time posture not found error"""
    def __init__(self, message: str = "Weekly time posture not found"):
        super().__init__(message, "404")