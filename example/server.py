""" 

"""

import sys
import os
import requests
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pkg_server import create_app


def main():
    create_app().run(debug=True, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
