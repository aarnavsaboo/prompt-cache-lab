import unittest
from prompt_cache_lab.trials import make_trials


class Tests(unittest.TestCase):
    def test_stable_prefix_hash(self):
        rows = make_trials(1000, 3, "stable")
        self.assertEqual(len({x.prefix_hash for x in rows}), 1)

    def test_mutation_changes_prefix(self):
        rows = make_trials(1000, 3, "mutated")
        self.assertGreater(len({x.prefix_hash for x in rows}), 1)


if __name__ == "__main__":
    unittest.main()
