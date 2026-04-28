"""Test suite for compression functionality with gitignore support."""

import os
import sys
import tempfile
import tarfile
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pkg_bulid.constructor import compress, parse_gitignore, ConfigFileNotFound, CompressionError


def test_parse_gitignore():
    """Test parsing .gitignore file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.gitignore', delete=False) as f:
            f.write("""# Comments should be ignored\n__pycache__/\n*.pyc\nbuild/\n.venv\n""")
            f.flush()
            
            patterns = parse_gitignore(f.name)
            assert '__pycache__/' in patterns
            assert '*.pyc' in patterns
            assert 'build/' in patterns
            assert '.venv' in patterns
            assert '# Comments should be ignored' not in patterns
    # remove the temporary file after the NamedTemporaryFile is closed
    os.unlink(f.name)


def test_parse_gitignore_missing_file():
    """Test parsing non-existent .gitignore file."""
    patterns = parse_gitignore('/nonexistent/.gitignore')
    assert patterns == set()
    print("[-] test_parse_gitignore_missing_file passed")


def test_compress_with_filters():
    """Test compression with gitignore filtering."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test structure
        os.makedirs(os.path.join(tmpdir, '__pycache__'))
        os.makedirs(os.path.join(tmpdir, 'src'))
        os.makedirs(os.path.join(tmpdir, 'build'))

        # Create files
        Path(os.path.join(tmpdir, 'src', 'main.py')).write_text('print("hello")')
        Path(os.path.join(tmpdir, '__pycache__', 'cache.pyc')).write_text('compiled')
        Path(os.path.join(tmpdir, 'file.txt')).write_text('text')
        Path(os.path.join(tmpdir, '.gitignore')).write_text('__pycache__/\nbuild/')

        # Compress
        output_file = os.path.join(tmpdir, 'test.tar.gz')
        compress(
            pkg_name='test_pkg',
            source_folder=tmpdir,
            output_file=output_file
        )

        # Verify archive
        assert os.path.exists(output_file)
        with tarfile.open(output_file, 'r:gz') as tar:
            names = tar.getnames()
            assert any('main.py' in name for name in names)
            assert any('file.txt' in name for name in names)
            # __pycache__ should be filtered out
            assert not any('__pycache__' in name for name in names)
            assert not any('.gitignore' in name for name in names)

        print("[-] test_compress_with_filters passed")


def test_compress_invalid_source():
    """Test compression with invalid source folder."""
    try:
        compress(
            pkg_name='test',
            source_folder='/nonexistent/path',
            output_file='test.tar.gz'
        )
        assert False, "Should have raised CompressionError"
    except CompressionError as e:
        assert "Source folder not found" in str(e)
        print("[-] test_compress_invalid_source passed")


def test_default_patterns_ignored():
    """Test that default patterns are always ignored."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create files that should always be ignored
        Path(os.path.join(tmpdir, '.git')).mkdir()
        Path(os.path.join(tmpdir, '.git', 'config')).write_text('git config')
        Path(os.path.join(tmpdir, 'test.tar.gz')).write_text('archive')
        Path(os.path.join(tmpdir, 'readme.txt')).write_text('readme')

        # No .gitignore file
        output_file = os.path.join(tmpdir, 'output.tar.gz')
        compress(
            pkg_name='test',
            source_folder=tmpdir,
            output_file=output_file
        )

        with tarfile.open(output_file, 'r:gz') as tar:
            names = tar.getnames()
            # .git should be filtered
            assert not any('.git' in name for name in names)
            # readme should be included
            assert any('readme.txt' in name for name in names)

        print("[-] test_default_patterns_ignored passed")


if __name__ == "__main__":
    print("Running compression tests...\n")
    try:
        test_parse_gitignore()
        test_parse_gitignore_missing_file()
        test_compress_with_filters()
        test_compress_invalid_source()
        test_default_patterns_ignored()
        print("\n[-] All tests passed!")
    except Exception as e:
        print(f"\n[x] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)