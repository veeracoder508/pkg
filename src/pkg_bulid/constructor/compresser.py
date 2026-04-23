import os
import tarfile
from pathlib import Path
from typing import Set
from .errors import CompressionError


def parse_gitignore(gitignore_path: str) -> Set[str]:
    """Parse .gitignore file and return a set of patterns to ignore.
    
    Args:
        gitignore_path: Path to .gitignore file
        
    Returns:
        Set of patterns to ignore
    """
    patterns = set()
    if not os.path.exists(gitignore_path):
        return patterns
    
    try:
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    patterns.add(line)
    except Exception as e:
        print(f"Warning: Could not read .gitignore: {e}")
    
    return patterns


def should_ignore(path: str, patterns: Set[str], root_path: str) -> bool:
    """Check if a path should be ignored based on gitignore patterns.
    
    Args:
        path: Path to check
        patterns: Set of patterns from .gitignore
        root_path: Root directory path
        
    Returns:
        True if path should be ignored, False otherwise
    """
    relative_path = os.path.relpath(path, root_path)
    path_obj = Path(relative_path)
    
    for pattern in patterns:
        pattern = pattern.rstrip('/')
        
        # Handle directory patterns (ending with /)
        if pattern.endswith('/'):
            if path_obj.name == pattern.rstrip('/'):
                return True
            if pattern.rstrip('/') in path.replace('\\', '/'):
                return True
        
        # Handle wildcard patterns
        if '*' in pattern:
            # Convert gitignore pattern to simple wildcard matching
            if '**' in pattern:
                # Match anywhere in path
                simplified = pattern.replace('**/', '').replace('**', '')
                if simplified in relative_path.replace('\\', '/'):
                    return True
            else:
                # Match filename or extension
                if pattern.startswith('*.'):
                    # Extension pattern like *.pyc
                    if path_obj.suffix == pattern.replace('*', ''):
                        return True
                elif '*' in pattern:
                    import fnmatch
                    if fnmatch.fnmatch(path_obj.name, pattern):
                        return True
        else:
            # Exact match
            if path_obj.name == pattern or relative_path.replace('\\', '/') == pattern:
                return True
    
    return False


def compress(pkg_name: str, source_folder: str = ".", output_file: str = "") -> None:
    """Compress a directory into a tar.gz file, respecting .gitignore patterns.
    
    Args:
        pkg_name: Name of the package (used as arcname)
        source_folder: Source directory to compress (default: current directory)
        output_file: Output tar.gz file path (default: {pkg_name}.tar.gz)
        
    Raises:
        CompressionError: If compression fails
    """
    try:
        if not output_file:
            output_file = f"{pkg_name}.tar.gz"
        
        # Get root path for relative calculations
        root_path = os.path.abspath(source_folder)
        
        if not os.path.exists(root_path):
            raise CompressionError(f"Source folder not found: {root_path}")
        
        # Ensure the output directory exists before creating the archive
        output_dir = os.path.dirname(os.path.abspath(output_file))
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Parse .gitignore patterns
        gitignore_path = os.path.join(root_path, '.gitignore')
        ignore_patterns = parse_gitignore(gitignore_path)
        
        # Add default patterns to always ignore
        ignore_patterns.update({
            '.git',
            '.gitignore',
            '.gitattributes',
            '*.tar.gz',
            '*.zip'
        })
        
        with tarfile.open(output_file, "w:gz") as tar:
            for root, dirs, files in os.walk(root_path):
                # Filter directories
                dirs[:] = [
                    d for d in dirs 
                    if not should_ignore(os.path.join(root, d), ignore_patterns, root_path)
                ]
                
                # Add files
                for file in files:
                    file_path = os.path.join(root, file)
                    if not should_ignore(file_path, ignore_patterns, root_path):
                        arcname = os.path.join(pkg_name, os.path.relpath(file_path, root_path))
                        tar.add(file_path, arcname=arcname)
    
    except CompressionError:
        raise
    except Exception as e:
        raise CompressionError(f"Failed to compress archive: {str(e)}")
