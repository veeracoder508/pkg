"""
Example usage of the package server client.

This script demonstrates how to publish packages to the server and 
search for existing packages using the Publisher class and API calls.
"""

import sys
import os
import requests
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pkg_bulid.publish import Publisher
from pkg_down import Downloader # Import the Downloader class


def example_publish_package():
    """Demonstrates how to publish a package to the server."""
    print("Example 1: Publishing a Package")
    print("-" * 50)
    
    # Initialize the publisher
    publisher = Publisher(base_url="http://localhost:5000")
    
    # Setup dummy package info
    pkg_name = "demo_package"
    version = "1.2.3"
    dummy_file = f"{pkg_name}-{version}.tar.gz"
    
    # Create a dummy file for the demonstration
    with open(dummy_file, "w") as f:
        f.write("This is a dummy package file for testing purposes.")
    
    try:
        print(f"Uploading {pkg_name} version {version}...")
        response = publisher.sendtoserver(pkg_name, version, dummy_file)
        print(f"[-] Server Response: {response}")
    except Exception as e:
        print(f"[x] Failed to publish: {e}")
    finally:
        # Clean up the dummy file
        if os.path.exists(dummy_file):
            os.remove(dummy_file)
    print()


def example_search_packages():
    """Demonstrates how to search for packages on the server."""
    print("Example 2: Searching for Packages")
    print("-" * 50)
    
    search_url = "http://localhost:5000/api/get/search"
    query = "demo"
    
    try:
        print(f"Searching for packages matching '{query}'...")
        response = requests.get(search_url, params={"name": query})
        
        if response.status_code == 200:
            data = response.json()
            print(f"[-] Found {data['count']} result(s):")
            for pkg in data['results']:
                print(f"  - {pkg['name']} (ID: {pkg['id']}, Latest: {pkg['latest_version']})")
        else:
            print(f"[x] Search failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[x] Error connecting to server: {e}")
    print()


def example_download_package():
    """Demonstrates how to download a package from the server."""
    print("Example 3: Downloading a Package")
    print("-" * 50)
    
    download_url = "http://localhost:5000/api/get/download"
    pkg_name = "demo_package"
    version = "1.2.3"
    
    try:
        print(f"Downloading {pkg_name} version {version}...")
        params = {"name": pkg_name, "version": version}
        response = requests.get(download_url, params=params, stream=True)
        
        if response.status_code == 200:
            output_filename = f"downloaded_{pkg_name}_{version}.tar.gz"
            with open(output_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"[-] Package downloaded successfully to: {output_filename}")
            
            # Clean up the downloaded file after demonstration
            if os.path.exists(output_filename):
                os.remove(output_filename)
        else:
            print(f"[x] Download failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[x] Error connecting to server: {e}")
    print()
    

def example_download_package_client():
    """Demonstrates how to download a package from the server using the Downloader class."""
    print("Example 4: Downloading a Package with Downloader Class")
    print("-" * 50)
    
    downloader = Downloader(base_url="http://localhost:5000")
    
    pkg_name = "demo_package"
    version = "1.2.3"
    
    try:
        print(f"Attempting to download {pkg_name} version {version}...")
        output_filename = downloader.download(pkg_name, version)
        print(f"[-] Package downloaded successfully to: {output_filename}")
        
        # Clean up the downloaded file after demonstration
        if os.path.exists(output_filename):
            os.remove(output_filename)
            print(f"  Cleaned up: {output_filename}")
            
    except FileNotFoundError as e:
        print(f"[x] Download failed: {e}")
    except Exception as e:
        print(f"[x] An unexpected error occurred: {e}")
    print()


if __name__ == "__main__":
    print("\nPackage Server Client Examples")
    print("Make sure your Flask server is running at http://localhost:5000\n")
    
    example_publish_package()
    example_search_packages()
    example_download_package() # This is the direct requests example
    example_download_package_client() # This uses the Downloader class