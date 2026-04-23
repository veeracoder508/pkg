"""Main builder functionality for creating package archives."""

import os
from pathlib import Path
from .errors import ConfigFileNotFound, CompressionError, BuildError
from .compresser import compress


CONFIG_FILES: tuple[str] = (
    "pyproject.toml",
    "README.md",
    ".python-version",
    "uv.lock",
    "LICENSE"
)

def check_if_all_config_files_exist() -> bool:
    """Check if all the config files for the package are present.

    Raises:
        ConfigFileNotFound: if any files are missing.

    Returns:
        bool: True if all the files are present.
    """
    files_not_found: list[str] = []
    for file in CONFIG_FILES:
        if not os.path.exists(file):
            files_not_found.append(file)
    if files_not_found:
        raise ConfigFileNotFound(str(files_not_found))
    return True


class Builder:
    """Builder class for compressing and packaging projects."""
    
    def __init__(self, pkg_name: str) -> None:
        """Initialize the builder with a package name.
        
        Args:
            pkg_name: Name of the package to build
        """
        self.pkg_name: str = pkg_name

    def build(self, output_dir: str = "wheels/") -> str:
        """Build the package archive respecting .gitignore patterns.
        
        Args:
            output_dir: Output directory for the archive (default: current directory)
            
        Returns:
            str: Path to the created archive
            
        Raises:
            ConfigFileNotFound: if required config files are missing
            CompressionError: if compression fails
            BuildError: if build operation fails
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
