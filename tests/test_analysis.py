import unittest

from reason_llm_guard.analysis import analyze
from reason_llm_guard.demo import generate_demo_records
from reason_llm_guard.schema import InterventionResult


class AnalysisTests(unittest.TestCase):
    def test_demo_exposes_prefix_effect_heterogeneity(self) -> None:
        report = analyze(generate_demo_records(samples=150, seed=7), bootstrap=500, seed=7)
        self.assertEqual(report.sample_count, 150)
        self.assertGreater(report.oracle_gap, 0.1)
        self.assertGreater(report.oracle_gap_ci_low, 0.0)

    def test_requires_paired_interventions(self) -> None:
        records = [
            InterventionResult("a", "benign", "P1", 0.0, 1.0, 0.0),
            InterventionResult("a", "benign", "P2", 0.0, 0.8, 0.0),
            InterventionResult("b", "harmful", "P1", 0.3, 0.7, 0.0),
        ]
        with self.assertRaisesRegex(ValueError, "same interventions"):
            analyze(records, bootstrap=10)


if __name__ == "__main__":
    unittest.main()

