from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Literal

Category = Literal["harmful", "benign", "mixed"]


@dataclass(frozen=True)
class InterventionResult:
    sample_id: str
    category: Category
    intervention: str
    unsafe: float
    utility: float
    cost: float
    response: str = ""

    def __post_init__(self) -> None:
        if not 0.0 <= self.unsafe <= 1.0:
            raise ValueError("unsafe must be in [0, 1]")
        if not 0.0 <= self.utility <= 1.0:
            raise ValueError("utility must be in [0, 1]")
        if self.cost < 0.0:
            raise ValueError("cost must be non-negative")


def read_jsonl(path: str | Path) -> list[InterventionResult]:
    records: list[InterventionResult] = []
    with Path(path).open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                records.append(InterventionResult(**json.loads(line)))
            except (TypeError, ValueError, json.JSONDecodeError) as exc:
                raise ValueError(f"invalid record at line {line_number}: {exc}") from exc
    return records


def write_jsonl(path: str | Path, records: Iterable[InterventionResult]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")

