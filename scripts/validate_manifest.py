#!/usr/bin/env python3
"""Check published artifact paths and JSON syntax without network access."""
import json
from pathlib import Path
import sys


def reject_constant(value):
    raise ValueError(f"Non-standard JSON number: {value}")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_constant)


def validate(root):
    root = root.resolve()
    manifest = read_json(root / "versions.json")
    if not isinstance(manifest, dict):
        raise ValueError("versions.json must contain an object")
    versions = manifest.get("versions")
    if not isinstance(versions, dict) or not versions:
        raise ValueError("versions must be a non-empty object")
    if not isinstance(manifest.get("latest"), str) or manifest["latest"] not in versions:
        raise ValueError("latest must name an entry in versions")
    checked = 0
    for version, artifacts in versions.items():
        if not isinstance(artifacts, dict) or not artifacts:
            raise ValueError(f"{version}: expected a non-empty artifact map")
        for name, relative in artifacts.items():
            if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
                raise ValueError(f"{version}/{name}: expected a relative artifact path")
            path = (root / relative).resolve()
            if root not in path.parents:
                raise ValueError(f"{version}/{name}: artifact path escapes the repository")
            try:
                read_json(path)
            except (OSError, UnicodeError, ValueError) as error:
                raise ValueError(f"{version}/{name}: {relative}: {error}") from error
            checked += 1
    return len(versions), checked


if __name__ == "__main__":
    try:
        versions, artifacts = validate(Path(__file__).resolve().parents[1])
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Manifest validation failed: {error}", file=sys.stderr)
        sys.exit(1)
    print(f"Validated {artifacts} JSON artifacts across {versions} versions.")
