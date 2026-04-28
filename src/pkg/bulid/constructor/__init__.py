"""Module for building and compressing Python packages.

Provides high-level Builder class and low-level utilities like compress, 
parse_gitignore, and configuration validation. Includes custom exceptions 
for error reporting.
"""


from .build import Builder, check_if_all_config_files_exist
from .compresser import compress, parse_gitignore
from .errors import ConfigFileNotFound, CompressionError, BuildError

__all__ = [
    "Builder",
    "compress",
    "parse_gitignore",
    "check_if_all_config_files_exist",
    "ConfigFileNotFound",
    "CompressionError",
    "BuildError",
]