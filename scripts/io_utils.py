"""Small helpers for stable UTF-8 text products across operating systems."""
from __future__ import annotations

from pathlib import Path


def write_text_lf(path: Path, text: str) -> None:
    """Write UTF-8 text with LF line endings and one trailing newline."""
    path.parent.mkdir(parents=True, exist_ok=True)
    canonical = text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n") + "\n"
    with path.open("w", encoding="utf-8", newline="\n") as destination:
        destination.write(canonical)


def canonicalise_text_file(path: Path) -> None:
    """Normalise an existing UTF-8 text product after a third-party writer."""
    text = path.read_text(encoding="utf-8")
    without_trailing_space = "\n".join(line.rstrip() for line in text.splitlines())
    write_text_lf(path, without_trailing_space)
