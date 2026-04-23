"""
Example usage of the builder with gitignore support.

This file demonstrates how to use the package builder to compress
your project while automatically excluding files specified in .gitignore
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pkg_bulid import Builder, ConfigFileNotFound, CompressionError, BuildError


def example_1_basic_build():
    """Example 1: Basic build with default output location."""
    print("Example 1: Basic Build")
    print("-" * 50)
    
    try:
        builder = Builder("my_awesome_package")
        output_file = builder.build()
        print(f"✓ Package built successfully!")
        print(f"  Output: {output_file}")
    except ConfigFileNotFound as e:
        print(f"✗ {e}")
    except Exception as e:
        print(f"✗ Error: {e}")
    print()


def example_2_custom_output_dir():
    """Example 2: Build with custom output directory."""
    print("Example 2: Custom Output Directory")
    print("-" * 50)
    
    try:
        builder = Builder("my_package")
        output_file = builder.build(output_dir="./dist")
        print(f"✓ Package built successfully!")
        print(f"  Output: {output_file}")
    except ConfigFileNotFound as e:
        print(f"✗ {e}")
    except Exception as e:
        print(f"✗ Error: {e}")
    print()


def example_3_error_handling():
    """Example 3: Comprehensive error handling."""
    print("Example 3: Error Handling")
    print("-" * 50)
    
    try:
        builder = Builder("my_package")
        output_file = builder.build()
        print(f"✓ Success: {output_file}")
    except ConfigFileNotFound as e:
        print(f"✗ Configuration Error: {e}")
    except CompressionError as e:
        print(f"✗ Compression Error: {e}")
    except BuildError as e:
        print(f"✗ Build Error: {e}")
    except Exception as e:
        print(f"✗ Unexpected Error: {e}")
    print()


def example_4_direct_compression():
    """Example 4: Direct compression without builder."""
    print("Example 4: Direct Compression")
    print("-" * 50)
    
    from pkg_bulid import compress
    
    try:
        compress(
            pkg_name="direct_package",
            source_folder=".",
            output_file="direct_package.tar.gz"
        )
        print("✓ Package compressed successfully!")
        print("  Ignored files from .gitignore: ✓")
    except CompressionError as e:
        print(f"✗ Compression Error: {e}")
    print()


def example_5_parsing_gitignore():
    """Example 5: Parse and inspect gitignore patterns."""
    print("Example 5: Inspect .gitignore Patterns")
    print("-" * 50)
    
    from src.pkg_bulid.constructor import parse_gitignore
    
    patterns = parse_gitignore(".gitignore")
    if patterns:
        print("Patterns found in .gitignore:")
        for i, pattern in enumerate(sorted(patterns), 1):
            print(f"  {i}. {pattern}")
    else:
        print("No .gitignore file found or it's empty")
    print()


def main():
    print("\n" + "=" * 50)
    print("Package Builder Examples with .gitignore Support")
    print("=" * 50 + "\n")
    
    # Run examples
    # Note: Uncomment the examples you want to run
    
    example_1_basic_build()
    example_5_parsing_gitignore()
    
    # example_2_custom_output_dir()
    # example_3_error_handling()
    # example_4_direct_compression()


if __name__ == "__main__":
    main()
