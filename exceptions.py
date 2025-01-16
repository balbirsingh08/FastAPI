from fastapi import HTTPException, status

class CustomHTTPException(HTTPException):
    """
    A custom exception class to standardize error handling.
    """
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        """
        Initialize the custom exception with a status code, detail message, and optional error code.
        
        Args:
        - status_code (int): HTTP status code.
        - detail (str): Error message.
        - error_code (str): Optional error code for better error categorization.
        """
        self.error_code = error_code
        super().__init__(status_code=status_code, detail=detail)
