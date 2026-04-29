import requests
import os
from pkg_server.utils.fs import ensure_parent_dir_and_touch
import tarfile


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

    def download(self, pkg_name: str, version: str, path: str = ".", unpack: bool = True) -> str:
        """
        Download a specific version of a package and save it locally.

        Args:
            pkg_name (str): The name of the package to download.
            version (str): The specific version string to retrieve.
            path (str): The directory to save the downloaded package.
            unpack (bool): To unpack the package or not. Defaults to True.

        Returns:
            str: The filename of the saved package archive.

        Raises:
            FileNotFoundError: If the package version does not exist on the server.
            Exception: If the server returns an unexpected error code.
        """
        url = f"{self.base_url}/api/get/download"
        params = {"name": pkg_name, "version": version}
        response = requests.get(url, params=params, stream=True)
        output_filename = os.path.join(path, f"{pkg_name}-{version}.tar.gz")

        if response.status_code == 200:
            # Determine a safe filename for the downloaded package
            # This assumes the server sends a filename in the Content-Disposition header,
            # or we can construct one based on pkg_name and version.
            # For simplicity, let's construct one.
            
            # Ensure destination directory and file exist
            ensure_parent_dir_and_touch(output_filename)

            with open(output_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            if unpack:
                # Ensure we have data and let tarfile auto-detect compression
                try:
                    if os.path.getsize(output_filename) == 0:
                        raise Exception("Downloaded file is empty")
                    with tarfile.open(output_filename, "r:*") as tar:
                        tar.extractall(path=path)
                except tarfile.ReadError as e:
                    raise Exception(f"Failed to unpack archive: {e}")

            return output_filename
        elif response.status_code == 404:
            raise FileNotFoundError(f"Package {pkg_name} version {version} not found on server.")
        else:
            raise Exception(f"Failed to download package (Status: {response.status_code}, Error: {response.text})")
        
    def list_versions(self, pkg_name: str) -> list:
        """list all the versions of the package.

        Args:
            pkg_name (str): The package name

        Returns:
            list: The list of packages.
        """
        url = f"{self.base_url}/api/get/versions"
        params = {"name": pkg_name}
        response = requests.get(url, params=params, stream=True)
        if response.status_code == 200:
            return response.json()["versions"]
        else:
            raise Exception(f"Failed to list versions (Status: {response.status_code}, Error: {response.text})")
