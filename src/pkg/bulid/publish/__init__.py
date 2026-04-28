import os
import requests


class Publisher:
    """Client for publishing packages to the package server."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        """_summary_

        Args:
            base_url (str, optional): The url for the package host. Defaults to "http://localhost:5000".
        """
        self.base_url = base_url.rstrip('/')

    def sendtoserver(self, pkg_name: str, version: str, file_path: str):
        """Upload the built package to the server.

        Args:
            pkg_name (str): The name of the package.
            version (str): The version of the package.
            file_path (str): The path to the compressed package file.

        Raises:
            FileNotFoundError: If the package file is not found.
            Exception

        Returns:
            Any
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Package file not found at: {file_path}")

        url = f"{self.base_url}/api/send/publish"
        
        with open(file_path, 'rb') as f:
            files = {'package': (os.path.basename(file_path), f, 'application/gzip')}
            data = {
                'name': pkg_name,
                'version': version
            }
            # Send the multi-part form data request
            response = requests.post(url, files=files, data=data)
            
        if response.status_code != 201:
            raise Exception(f"Publish failed ({response.status_code}): {response.text}")
            
        return response.json()
