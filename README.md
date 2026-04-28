# Package Downloader & Registry

A full-stack Python package management system featuring a local build engine, a Flask-based registry server, and a client-side SDK for publishing and downloading.

## Features

- **Build Engine**: Create `.tar.gz` packages while respecting `.gitignore` patterns.
- **Registry Server**: A Flask API with a SQLite backend to manage package metadata and storage.
- **Secure Storage**: Automatic filename sanitization and secure file serving.
- **Client SDKs**: Easy-to-use `Publisher` and `Downloader` classes for automation.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Start the Registry Server
```bash
python -m pkg_server.app
```

### 2. Build and Publish a Package
```python
from pkg_bulid import Builder
from pkg_bulid.publish import Publisher

builder = Builder("my_pkg")
archive = builder.build()

publisher = Publisher(base_url="http://localhost:5000") # Replace it with the url for the server.
publisher.sendtoserver("my_pkg", "1.0.0", archive) # Replace it with your package.
```

### 3. Search and Download
```python
from pkg_down import Downloader

downloader = Downloader(base_url="http://localhost:5000") # Replace it with the url for the server.
downloader.download("my_pkg", "1.0.0") # Replace it with your package.
```

## Documentation

- Architecture Guide - Deep dive into logic and data flow.
- Quick Start Guide - Detailed usage examples.
- Change Log - History of features and fixes.

## License
MIT