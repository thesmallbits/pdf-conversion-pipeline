from pathlib import Path


def assert_file(_path: Path):
    if not _path.exists():
        raise ValueError(f"{_path} doest not exists")
    if not _path.is_file():
        raise ValueError(f"{_path} must be a file")


def assert_dir(_path: Path):
    if not _path.exists():
        raise ValueError(f"{_path} does not exists")
    if not _path.is_dir():
        raise ValueError(f"{_path} must be a directory")
