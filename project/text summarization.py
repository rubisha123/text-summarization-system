import unittest
from utils import extractive_summarize

class TestSummarization(unittest.TestCase):
    def test_extractive_summary(self):
        text = "This is sentence 1. This is sentence 2. This is sentence 3."
        summary = extractive_summarize(text, n_sentences=2)
        self.assertEqual(len(summary.split(". ")), 2)

if __name__ == "__main__":
    unittest.main()
