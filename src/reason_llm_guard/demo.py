from __future__ import annotations

import random

from .schema import InterventionResult

INTERVENTIONS = ("no_prefix", "P1", "P2", "P3", "P4")
CATEGORIES = ("harmful", "benign", "mixed")


def generate_demo_records(samples: int = 150, seed: int = 42) -> list[InterventionResult]:
    """Generate heterogeneous synthetic effects for pipeline validation only."""
    if samples < 1:
        raise ValueError("samples must be positive")
    rng = random.Random(seed)
    records: list[InterventionResult] = []
    preferred = {"harmful": "P3", "benign": "P1", "mixed": "P4"}

    for index in range(samples):
        category = CATEGORIES[index % len(CATEGORIES)]
        best = preferred[category]
        for intervention in INTERVENTIONS:
            mismatch = 0.0 if intervention == best else 0.22
            if intervention == "no_prefix":
                mismatch += 0.18 if category != "benign" else 0.02
            unsafe_base = 0.08 if category == "benign" else 0.18
            utility_base = 0.92 if category == "benign" else 0.82
            unsafe = min(1.0, max(0.0, unsafe_base + mismatch + rng.uniform(-0.04, 0.04)))
            utility = min(1.0, max(0.0, utility_base - mismatch + rng.uniform(-0.04, 0.04)))
            cost = 0.0 if intervention == "no_prefix" else 0.03 + rng.uniform(0.0, 0.02)
            records.append(
                InterventionResult(
                    sample_id=f"pilot-{index:04d}",
                    category=category,  # type: ignore[arg-type]
                    intervention=intervention,
                    unsafe=unsafe,
                    utility=utility,
                    cost=cost,
                )
            )
    return records

