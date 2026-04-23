"""Custom exceptions for the constructor module."""


class ConfigFileNotFound(Exception):
    """Raised when required configuration file is not found."""
    
    def __init__(self, file: str) -> None:
        message: str = f"Config file not found: {file}"
        super().__init__(message)


class CompressionError(Exception):
    """Raised when compression operation fails."""
    
    def __init__(self, message: str) -> None:
        super().__init__(f"Compression error: {message}")


class BuildError(Exception):
    """Raised when build operation fails."""
    
    def __init__(self, message: str) -> None:
        super().__init__(f"Build error: {message}")
