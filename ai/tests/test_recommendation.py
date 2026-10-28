"""
Unit tests for AI Engineer Learning OS Prerequisite-Aware Recommendation Engine.
"""

import unittest
import tempfile
import os
from backend.database import init_db, get_all_progress, update_topic_progress
from backend.recommendation import recommend_next_topic, explain_prerequisite_tree


class TestRecommendation(unittest.TestCase):

    def setUp(self):
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        init_db(self.temp_db_path)

    def tearDown(self):
        os.close(self.temp_db_fd)
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def test_fresh_start_recommends_foundation(self):
        """When starting fresh with 0 progress, must recommend Stage 1 root topic (e.g. py_syntax)."""
        data = get_all_progress(self.temp_db_path)
        rec = recommend_next_topic(data)

        rec_topic = rec["recommended_topic"]
        self.assertIn(rec_topic["id"], ["py_syntax", "py_terminal"])
        self.assertEqual(rec_topic["stage_id"], 1)
        self.assertIn("Essential Foundation", rec["reason"])
        self.assertEqual(len(rec["satisfied_prerequisites"]), 0)

    def test_prerequisite_progression(self):
        """When py_syntax is mastered, it should unlock py_operators or subsequent Stage 1 topic."""
        update_topic_progress(
            topic_id="py_syntax",
            status="mastered",
            confidence_rating=5,
            db_path=self.temp_db_path
        )
        data = get_all_progress(self.temp_db_path)
        rec = recommend_next_topic(data)
        rec_topic = rec["recommended_topic"]

        # py_operators requires py_syntax
        self.assertEqual(rec_topic["id"], "py_operators")
        self.assertEqual(rec_topic["stage_id"], 1)
        self.assertGreater(len(rec["satisfied_prerequisites"]), 0)
        self.assertEqual(rec["satisfied_prerequisites"][0]["id"], "py_syntax")

    def test_never_recommends_advanced_without_prerequisites(self):
        """Advanced topics (like snn_transformers or adv_lora_peft) must NEVER be recommended to a beginner."""
        data = get_all_progress(self.temp_db_path)
        rec = recommend_next_topic(data)
        self.assertNotIn(rec["recommended_topic"]["id"], ["snn_transformers", "adv_lora_peft", "rag_vector_db"])

    def test_prioritizes_needs_revision(self):
        """If a topic is marked as needs_revision, it should take precedence for review."""
        update_topic_progress(
            topic_id="py_syntax",
            status="needs_revision",
            confidence_rating=1,
            db_path=self.temp_db_path
        )
        data = get_all_progress(self.temp_db_path)
        rec = recommend_next_topic(data)
        self.assertEqual(rec["recommended_topic"]["id"], "py_syntax")
        self.assertIn("Reinforcement Required", rec["reason"])

    def test_prerequisite_tree_explanation(self):
        """Explains full dependency chain up to root."""
        data = get_all_progress(self.temp_db_path)
        tree = explain_prerequisite_tree("snn_transformers", data["topics_progress"])
        self.assertEqual(tree["target_topic"]["id"], "snn_transformers")
        chain_ids = [item["id"] for item in tree["prerequisites_chain"]]
        self.assertIn("snn_attention", chain_ids)
        self.assertFalse(tree["all_satisfied"])


if __name__ == "__main__":
    unittest.main()

