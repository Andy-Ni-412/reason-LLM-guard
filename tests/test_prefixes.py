import unittest
from pathlib import Path

from reason_llm_guard.prefixes import load_prefixes


class PrefixLibraryTests(unittest.TestCase):
    def test_library_contains_control_and_four_prefixes(self) -> None:
        path = Path(__file__).parents[1] / "configs" / "prefixes.json"
        library = load_prefixes(path)
        self.assertEqual(set(library), {"no_prefix", "P1", "P2", "P3", "P4"})
        self.assertTrue(all(library[item].text for item in ("P1", "P2", "P3", "P4")))


if __name__ == "__main__":
    unittest.main()

