"""Server-side implementation of the package registry.

This package encapsulates all server-side logic, including the Flask 
application initialization, database configuration, and the API routes 
for package discovery and distribution.
"""

from .server.app import create_app

__version__ = '0.0.1'
