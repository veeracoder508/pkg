"""Main entry point for package building."""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pkg_bulid import Bulider, ConfigFileNotFound, CompressionError, BuildError


def main():
    """Build a package archive respecting .gitignore patterns."""
    try:
        builder = Bulider("package_downloader")
        output_file = builder.build()
        print(f"✓ Package built successfully: {output_file}")
    except ConfigFileNotFound as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    except (CompressionError, BuildError) as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
