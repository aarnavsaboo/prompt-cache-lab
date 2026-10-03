import unittest
from prompt_cache_lab.planner import expand
from prompt_cache_lab.runner import build_prompt
from prompt_cache_lab.conversation import conversation_prompts


class Tests(unittest.TestCase):
    def test_matrix(self):
        rows = expand({
            "modes":["stable","mutated"], "prefix_chars":[100,200],
            "suffix_chars":[20], "output_tokens":[10], "requests_per_cell":2
        })
        self.assertEqual(len(rows), 8)

    def test_stable_prompt_keeps_prefix(self):
        row = expand({"modes":["stable"],"prefix_chars":[100],"suffix_chars":[20],"output_tokens":[10],"requests_per_cell":1})[0]
        prompt, prefix = build_prompt(row)
        self.assertTrue(prompt.startswith(prefix))

    def test_conversation_grows(self):
        rows = conversation_prompts(3, 100)
        self.assertLess(len(rows[0]), len(rows[-1]))


if __name__ == "__main__":
    unittest.main()
