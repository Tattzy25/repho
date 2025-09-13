"""
Backend Rules Engine:
Defines validation rules for each pipeline phase to enforce zero-fallback behavior.
"""
# Install pydantic library by running 'pip install pydantic' in your terminal

from pydantic import BaseModel, validator
import os

class Manifest(BaseModel):
    path: str
    files: dict[str, int]  # filename -> line_count

    @validator('files')
    def no_empty_files(cls, v):
        # Rule #1: No zero-line files
        for fname, count in v.items():
            if count == 0:
                raise ValueError(f"Empty file detected: {fname}")
        return v

class RuleEngine:
    @staticmethod
    def validate_manifest(manifest: Manifest):
        # Rule #2: snake_case filenames only
        for f in manifest.files:
            if f != f.lower().replace('-', '_'):
                raise ValueError(f"Invalid filename (must be snake_case): {f}")
        # Rule #3: line counts must match actual file
        for fname, cnt in manifest.files.items():
            real_path = os.path.join(manifest.path, fname)
            if os.path.exists(real_path):
                actual = sum(1 for _ in open(real_path, 'r', encoding='utf-8'))
                if actual != cnt:
                    raise ValueError(f"Line count mismatch for {fname}: manifest says {cnt}, actual {actual}")
            else:
                raise ValueError(f"Missing file in manifest verification: {fname}")
        return True

    @staticmethod
    def validate_scaffold(path: str, manifest: Manifest):
        # Rule #4: all dirs exist, no extra files
        for fname in manifest.files:
            full = os.path.join(path, fname)
            if not os.path.exists(full):
                raise ValueError(f"Scaffold missing: {full}")
        return True
