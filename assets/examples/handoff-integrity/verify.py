"""Public, synthetic file-integrity example. Python 3.10+; no dependencies.

Run: python verify.py
Exercise changed, missing, unexpected, and invalid inputs: python verify.py --self-test
This is a standalone teaching example, not an extract of the RA runtime.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
from tempfile import TemporaryDirectory

FILES = ("sample/source-note.txt", "sample/method-note.txt")


# BEGIN PUBLIC EXCERPT
def inspect_file(path: Path, expected_hash: str) -> str:
    if path.is_symlink():
        return "REJECTED LINK"
    if not path.is_file():
        return "MISSING"
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return "MATCH" if digest.hexdigest() == expected_hash else "CHANGED"
# END PUBLIC EXCERPT


def verify(root: Path) -> list[str]:
    """Read the fixed sample folder; return discrepancies without changing files."""
    try:
        manifest_path = root / "manifest.json"
        sample = root / "sample"
        if manifest_path.is_symlink() or sample.is_symlink():
            return ["REJECTED LINK: manifest or sample folder"]
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if (not isinstance(manifest, dict)
                or set(manifest) != {"format", "files"}
                or manifest["format"] != "portfolio-integrity-example/1"
                or not isinstance(manifest["files"], dict)
                or set(manifest["files"]) != set(FILES)):
            return ["INVALID MANIFEST: expected the two named sample files"]
        expected = manifest["files"]
        if any(not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value)
               for value in expected.values()):
            return ["INVALID MANIFEST: SHA-256 values must be 64 lowercase hexadecimal characters"]
        issues = []
        if sample.is_dir():
            for path in sorted(sample.iterdir()):
                if "sample/" + path.name not in FILES:
                    issues.append("UNEXPECTED: sample/" + path.name)
        for name in FILES:
            status = inspect_file(root / name, expected[name])
            if status != "MATCH":
                issues.append(status + ": " + name)
        return issues
    except (OSError, UnicodeError, ValueError) as error:
        # Report the failure category without printing machine-specific paths.
        return ["UNREADABLE PACKAGE: " + type(error).__name__]


def self_test(source: Path) -> None:
    """Change temporary copies only. The downloaded sample stays untouched."""
    baseline = verify(source)
    if baseline:
        raise RuntimeError("Start with an intact download: " + "; ".join(baseline))
    with TemporaryDirectory(prefix="portfolio-integrity-") as directory:
        root = Path(directory)
        (root / "sample").mkdir()
        for name in ("manifest.json", *FILES):
            shutil.copyfile(source / name, root / name)
        assert verify(root) == [], "Intact files must match"
        print("PASS: intact sample matches its manifest")
        note = root / FILES[0]
        original = note.read_bytes()
        note.write_bytes(original + b"Changed in the temporary test copy.\n")
        assert verify(root) == ["CHANGED: " + FILES[0]], "Changed bytes must be detected"
        print("PASS: changed file is detected")
        note.unlink()
        assert verify(root) == ["MISSING: " + FILES[0]], "Missing file must be detected"
        print("PASS: missing file is detected")
        note.write_bytes(original)
        extra = root / "sample/extra.txt"
        extra.write_text("Synthetic extra file.\n", encoding="utf-8")
        assert verify(root) == ["UNEXPECTED: sample/extra.txt"], "Unexpected file must be detected"
        print("PASS: unexpected file is detected")
        extra.unlink()
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        manifest["files"][FILES[0]] = "invalid"
        (root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        assert verify(root)[0].startswith("INVALID MANIFEST:"), "Malformed digest must be rejected"
        print("PASS: malformed manifest is rejected")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    if args.self_test:
        try:
            self_test(root)
        except (AssertionError, RuntimeError, OSError) as error:
            print("FAIL:", str(error))
            return 1
        return 0
    issues = verify(root)
    print("\n".join(issues) if issues else "MATCH: both sample files match the supplied manifest")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
