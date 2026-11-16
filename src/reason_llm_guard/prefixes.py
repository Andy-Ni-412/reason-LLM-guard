from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Prefix:
    id: str
    name: str
    purpose: str
    text: str


def load_prefixes(path: str | Path) -> dict[str, Prefix]:
    """Load a versioned Prefix Library and reject duplicate identifiers."""
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    prefixes = [Prefix(**item) for item in payload["prefixes"]]
    library = {prefix.id: prefix for prefix in prefixes}
    if len(library) != len(prefixes):
        raise ValueError("prefix IDs must be unique")
    if "no_prefix" not in library:
        raise ValueError("Prefix Library must include the no_prefix control")
    return library

