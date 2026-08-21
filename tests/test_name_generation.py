import importlib.util
import random as stdlib_random
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "random.py"
SPEC = importlib.util.spec_from_file_location("company_name_researcher", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class NameGenerationTests(unittest.TestCase):
    def test_seeded_candidate_has_meaningful_metadata(self):
        candidate = MODULE.generate_candidate(stdlib_random.Random(7))

        self.assertRegex(candidate["name"], r"^[a-z]{5,15}$")
        self.assertIn(candidate["style"], {"direct", "blend", "transform"})
        self.assertTrue(candidate["roots"])
        self.assertEqual(len(candidate["roots"]), len(candidate["meanings"]))
        self.assertEqual(len(candidate["roots"]), len(candidate["languages"]))

    def test_semantic_score_rewards_known_roots(self):
        meaningful = MODULE.name_quality("lumora", semantic_bonus=15)
        phonetic = MODULE.name_quality("brxqzt", semantic_bonus=0)

        self.assertGreater(meaningful, phonetic)


if __name__ == "__main__":
    unittest.main()
