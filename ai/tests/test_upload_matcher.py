"""
Unit tests for AI Engineer Learning OS Upload Parser & Concept Matcher.
"""

import unittest
from backend.upload_parser import extract_text_from_content, match_concepts_to_roadmap


class TestUploadMatcher(unittest.TestCase):

    def test_text_extraction_plain_file(self):
        sample = b"# PyTorch Neural Network Notes\nWe compute dot product between vectors and backpropagation gradients."
        text, p_type, diag = extract_text_from_content(sample, "notes.md")
        self.assertIn("PyTorch Neural Network Notes", text)
        self.assertEqual(p_type, "text_md")

    def test_three_group_concept_matching(self):
        sample_text = """
        Study Session:
        Today we reviewed Python syntax and variables.
        Then we studied the Transformer architecture and self-attention Query, Key, and Value matrices.
        Finally we computed dot products and cosine similarity.
        """
        # User has only mastered py_syntax; snn_transformers has unsatisfied prerequisites
        progress_map = {
            "py_syntax": {"status": "mastered", "confidence_rating": 4, "last_studied_date": "2026-10-01"}
        }

        matched = match_concepts_to_roadmap(sample_text, progress_map)

        group_a = matched["group_a_found"]
        group_b = matched["group_b_already_learned"]
        group_c = matched["group_c_missing_or_further_study"]

        # Group A should contain found topics
        found_ids = [item["topic_id"] for item in group_a]
        self.assertIn("py_syntax", found_ids)
        self.assertIn("snn_transformers", found_ids)
        self.assertIn("math_dot_products", found_ids)

        # Group B should identify py_syntax as already learned
        learned_ids = [item["topic_id"] for item in group_b]
        self.assertIn("py_syntax", learned_ids)

        # Group C should identify missing prerequisites for advanced topics found
        missing_ids = [item["topic_id"] for item in group_c]
        self.assertIn("snn_attention", missing_ids)


if __name__ == "__main__":
    unittest.main()

