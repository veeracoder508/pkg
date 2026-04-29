"""
Example usage of the package downloader client.

This script demonstrates how to download packages from the server
using the Downloader class.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pkg.down import Downloader


def example_download_package_client():
    """Demonstrates how to download a package from the server using the Downloader class."""
    print("Example: Downloading a Package with Downloader Class")
    print("-" * 50)
    
    downloader = Downloader(base_url="http://localhost:5000")
    
    pkg_name = "pkg++"
    version = "0.0.0"
    
    try:
        print(f"Attempting to download {pkg_name} version {version}...")
        output_filename = downloader.download(pkg_name, version, path="downloads")
        print(f"[-] Package downloaded successfully to: {output_filename}")
            
    except FileNotFoundError as e:
        print(f"[x] Download failed: {e}")
    except Exception as e:
        print(f"[x] An unexpected error occurred: {e}")
    print()


if __name__ == "__main__":
    print("\nPackage Downloader Client Example")
    print("Make sure your Flask server is running at http://localhost:5000\n")
    example_download_package_client()