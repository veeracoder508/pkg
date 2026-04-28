import requests
import os


class Downloader: 
    """
    A client for downloading packages from the package registry server.

    Handles HTTP requests to the registry API and streams the package 
    contents directly to the local filesystem.
    """
    def __init__(self, base_url: str = "http://localhost:5000"):
        """
        Initialize the Downloader with the registry server's base URL.

        Args:
            base_url (str): The URL of the registry server.
        """
        self.base_url = base_url.rstrip('/')

    def download(self, pkg_name: str, version: str):
        """
        Download a specific version of a package and save it locally.

        Args:
            pkg_name (str): The name of the package to download.
            version (str): The specific version string to retrieve.

        Returns:
            str: The filename of the saved package archive.

        Raises:
            FileNotFoundError: If the package version does not exist on the server.
            Exception: If the server returns an unexpected error code.
        """
        url = f"{self.base_url}/api/get/download"
        params = {"name": pkg_name, "version": version}
        response = requests.get(url, params=params, stream=True)

        if response.status_code == 200:
            # Determine a safe filename for the downloaded package
            # This assumes the server sends a filename in the Content-Disposition header,
            # or we can construct one based on pkg_name and version.
            # For simplicity, let's construct one.
            output_filename = f"{pkg_name}-{version}.tar.gz"
            
            with open(output_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return output_filename
        elif response.status_code == 404:
            raise FileNotFoundError(f"Package {pkg_name} version {version} not found on server.")
        else:
            raise Exception(f"Failed to download package (Status: {response.status_code}, Error: {response.text})")
        