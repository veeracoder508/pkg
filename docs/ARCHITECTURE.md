# Architecture & Design Guide

## Module Architecture

```
┌──────────────────────────────────────────────────────────┐
│                      main.py (CLI)                       │
│  - Entry point for command-line interface                │
│  - Error handling and user feedback                      │
└────────────────┬─────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────┐
│            pkg_bulid (Package Builder)                   │
│  Exports: Bulider, compress, errors                      │
└────────────────┬─────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────┐
│         constructor (Core Implementation)                │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────────────────────────────────┐         │
│  │  build.py - Bulider Class                   │         │
│  │  ├─ __init__(pkg_name)                      │         │
│  │  └─ build(output_dir) -> str                │         │
│  │                                             │         │
│  │  check_if_all_config_files_exists() -> bool │         │
│  └─────────────────────────────────────────────┘         │
│                                                          │
│  ┌─────────────────────────────────────────────┐         │
│  │  compresser.py - Compression Engine         │         │
│  │  ├─ parse_gitignore(path) -> Set[str]       │         │
│  │  ├─ should_ignore(path, patterns) -> bool   │         │
│  │  └─ compress(pkg_name, src, out) -> None    │         │
│  └─────────────────────────────────────────────┘         │
│                                                          │
│  ┌─────────────────────────────────────────────┐         │
│  │  errors.py - Exception Classes              │         │
│  │  ├─ ConfigFileNotFound                      │         │
│  │  ├─ CompressionError                        │         │
│  │  └─ BuildError                              │         │
│  └─────────────────────────────────────────────┘         │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
User Input (CLI)
    │
    ▼
main.py
    │
    ├─ Create Bulider instance
    │
    ▼
Bulider.build()
    │
    ├─ check_if_all_config_files_exists()
    │  └─ Validates: pyproject.toml, README.md, etc.
    │
    ▼  (if all exist)
    │
    ├─ Call compress()
    │
    ▼
compress()
    │
    ├─ parse_gitignore(".gitignore")
    │  └─ Returns: Set[str] patterns
    │
    ├─ Add default ignore patterns
    │  └─ .git, .gitignore, *.tar.gz, *.zip
    │
    ├─ os.walk() with filtering
    │  ├─ For each directory:
    │  │  └─ Filter using should_ignore()
    │  │
    │  └─ For each file:
    │     ├─ Check should_ignore()
    │     └─ Add to tarfile if not ignored
    │
    ▼
output.tar.gz
    │
    ▼
Success Message & Exit
```

## Pattern Matching Algorithm

```python
should_ignore(path, patterns, root_path):
    
    1. Get relative path from root
    2. Create Path object for cross-platform support
    
    3. For each pattern in patterns:
    
        a) Strip trailing slashes
        
        b) If pattern contains '/':
           └─ Check if it's a directory pattern
        
        c) If pattern contains '*':
        
           - '**.ext' → Match anywhere in path
           - '*.ext'  → Match filename extension
           - '*name'  → Use fnmatch for wildcards
        
        d) Otherwise:
           └─ Exact filename/path match
    
    4. Return True if any pattern matches
```

## Configuration Files

### Required Files (checked by `check_if_all_config_files_exists`)
```
pyproject.toml      # Python project configuration
README.md           # Project documentation
.python-version     # Python version specification
uv.lock            # uv package manager lockfile
```

### .gitignore Patterns (example)
```ini
# Python-generated files
__pycache__/
*.py[oc]           # .pyc and .pyo files
build/
dist/
wheels/
*.egg-info

# Virtual environments
.venv
```

## Error Handling Flow

```
try:
    builder.build()
    
except ConfigFileNotFound:
    │
    └─ Missing required config file
       └─ Exit code: 1
    
except CompressionError:
    │
    └─ Compression operation failed
       ├─ Source folder doesn't exist
       ├─ Permission denied
       └─ Disk space issues
       └─ Exit code: 1
    
except BuildError:
    │
    └─ Build operation failed
       ├─ Unknown compression error
       └─ Exit code: 1
    
except Exception:
    │
    └─ Unexpected system error
       └─ Exit code: 1
```

## Type Annotations

All public functions and classes use full type hints:

```python
# Builder class
class Bulider:
    def __init__(self, pkg_name: str) -> None: ...
    def build(self, output_dir: str = ".") -> str: ...

# Utility functions
def parse_gitignore(gitignore_path: str) -> Set[str]: ...
def should_ignore(path: str, patterns: Set[str], root_path: str) -> bool: ...
def compress(pkg_name: str, source_folder: str = ".", output_file: str = "") -> None: ...

# Functions with validation
def check_if_all_config_files_exists() -> bool: ...
```

## Performance Considerations

1. **Directory Filtering**
   - Directories are filtered in `os.walk()` using `dirs[:] = [...]`
   - This prevents traversing ignored directories entirely
   - Saves I/O and memory for large projects

2. **Pattern Set Usage**
   - Uses `Set[str]` for O(1) lookup on exact matches
   - Wildcard patterns use regex/fnmatch for matching

3. **Memory Usage**
   - Streams files to tarfile (no full file loading)
   - Only stores pattern set in memory (typically small)

4. **Cross-Platform**
   - Uses `os.path` instead of hardcoded paths
   - Handles Windows backslashes and Unix forward slashes

## Extension Points

### Adding Custom Patterns
```python
from src.pkg_bulid.constructor import parse_gitignore

patterns = parse_gitignore(".gitignore")
patterns.add(".myignore")  # Add custom pattern
```

### Custom Compression Logic
```python
from src.pkg_bulid.constructor.compresser import compress

# Extend compress() by wrapping:
def custom_compress(pkg_name: str) -> None:
    compress(pkg_name=pkg_name)
    # Add post-compression logic
```

### Error Subclassing
```python
from src.pkg_bulid.constructor.errors import BuildError

class CustomBuildError(BuildError):
    pass
```

## Testing Strategy

Test files are located in `tests/test_compression.py`:

1. **Unit Tests**
   - `test_parse_gitignore()` - Pattern parsing
   - `test_parse_gitignore_missing_file()` - Error handling
   - `test_compress_invalid_source()` - Validation

2. **Integration Tests**
   - `test_compress_with_filters()` - Full compression flow
   - `test_default_patterns_ignored()` - Default filtering

3. **Coverage Areas**
   - Pattern matching logic
   - Directory/file filtering
   - Error conditions
   - Archive contents validation

## Future Enhancements

Potential improvements:

1. **Advanced .gitignore Features**
   - Negation patterns (!)
   - Prefix patterns (^)
   - Trailing slash semantics

2. **Performance**
   - Async compression for large files
   - Progress callbacks
   - Multi-threading for I/O

3. **Features**
   - Multiple archive formats (zip, 7z)
   - Incremental backups
   - Compression level control
   - Archive encryption

4. **SDK**
   - Configuration file support
   - Plugin system
   - Custom filters
