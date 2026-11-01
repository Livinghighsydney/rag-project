import hashlib
from collections import defaultdict


def hash_file(file_path: str) -> str:
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(8192), b""):
            sha256.update(block)
    return sha256.hexdigest()


def detect_duplicates(file_paths: list[str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for path in file_paths:
        groups[hash_file(path)].append(path)
    return {h: paths for h, paths in groups.items() if len(paths) > 1}
