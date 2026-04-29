"""Filesystem helper utilities."""
from pathlib import Path
import os
from typing import Union


def ensure_parent_dir_and_touch(path: Union[str, Path]) -> None:
    """Ensure the parent directory exists and create the file if missing.

    This is a best-effort helper: it will create missing parent directories
    and touch the file so callers that expect the path to be present can proceed.
    Exceptions are swallowed to avoid breaking callers in non-critical paths.
    """
    p = Path(path)
    parent = p.parent
    if parent and not parent.exists():
        try:
            os.makedirs(parent, exist_ok=True)
        except Exception:
            return

    try:
        p.touch(exist_ok=True)
    except Exception:
        return
