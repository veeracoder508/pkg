"""Main builder functionality for creating package archives."""

import os
from pathlib import Path
from .errors import ConfigFileNotFound, CompressionError, BuildError
from .compresser import compress


CONFIG_FILES: tuple[str, ...] = (
    "pyproject.toml",
    "README.md",
    ".python-version",
    "uv.lock",
    "LICENSE"
)
"""All the configration files needed for the package."""

def check_if_all_config_files_exist() -> bool:
    """Check if all the config files for the package are present.
    
    Iterates through CONFIG_FILES and verifies their existence in the current directory.

    Returns:
        bool: True if all required configuration files are found.

    Raises:
        ConfigFileNotFound: If one or more specified configuration files are missing.
    """
    files_not_found: list[str] = []
    for file in CONFIG_FILES:
        if not os.path.exists(file):
            files_not_found.append(file)
    if files_not_found:
        raise ConfigFileNotFound(str(files_not_found))
    return True


class Builder: 
    """
    Manages the building and archiving of a project into a distributable package.

    This class orchestrates the process of creating a `.tar.gz` archive,
    respecting `.gitignore` patterns and validating the presence of essential
    configuration files before compression.
    """
    def __init__(self, pkg_name: str) -> None:
        """Initialize the builder with a package name.
        
        Args:
            pkg_name (str): The name of the package to be built.
        """
        self.pkg_name: str = pkg_name

    def build(self, output_dir: str = "wheels/") -> str:
        """Build the package archive respecting .gitignore patterns.
        
        Validates configuration, creates the output directory, and compresses 
         the project into a .tar.gz archive.

        Args:
            output_dir (str): Directory where the archive will be saved. Defaults to "wheels/".

        Returns:
            str: The absolute path to the newly created package archive file.

        Raises:
            ConfigFileNotFound: If required configuration files are missing.
            CompressionError: If compression fails.
            BuildError: If any other unexpected error occurs during the build.
        """
        try:
            if check_if_all_config_files_exist():
                os.makedirs(output_dir, exist_ok=True)
                output_file = os.path.join(output_dir, f"{self.pkg_name}.tar.gz")
                compress(pkg_name=self.pkg_name, source_folder=".", output_file=output_file)
                return output_file
            return ""
        except ConfigFileNotFound:
            raise
        except CompressionError:
            raise
        except Exception as e:
            raise BuildError(f"Failed to build package: {str(e)}")
