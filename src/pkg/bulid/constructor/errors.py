"""Custom exceptions for the constructor module."""


class ConfigFileNotFound(Exception): 
    """Exception raised when a required configuration file is not found.

    This typically occurs during the build process if essential files like
    `pyproject.toml` or `README.md` are missing from the project directory.
    """
    def __init__(self, file: str) -> None:
        """Initialize the ConfigFileNotFound exception.

        Args:
            file (str): The name or path of the configuration file not found.
        """
        message: str = f"Config file not found: {file}"
        super().__init__(message)


class CompressionError(Exception): 
    """Exception raised when a compression operation fails.

    This can indicate issues such as the source directory not existing,
    permissions problems, or errors during the creation of the archive file.
    """
    def __init__(self, message: str) -> None:
        """Initialize the CompressionError exception.

        Args:
            message (str): Reason for the compression failure.
        """
        super().__init__(f"Compression error: {message}")


class BuildError(Exception): 
    """Exception raised when a general build operation fails.

    This is a generic exception for build-related failures not specifically
    covered by `ConfigFileNotFound` or `CompressionError`, catching broader
    issues during the package construction process.
    """
    def __init__(self, message: str) -> None:
        """Initialize the BuildError exception.

        Args:
            message (str): Reason for the build failure.
        """
        super().__init__(f"Build error: {message}")
