"""
In-process end-to-end integration tests for backend server endpoints and request handling.
Runs without requiring external TCP network permissions.
"""

import unittest
import json
import tempfile
import os

from backend.database import (
    init_db,
    get_all_progress,
    update_topic_progress,
    record_quiz_attempt,
    record_project_progress,
    export_database_json,
    import_database_json,
    reset_learning_data
)
from backend.roadmap_data import STAGES, TOPICS, get_topic_by_id
from backend.recommendation import recommend_next_topic, explain_prerequisite_tree
from backend.upload_parser import extract_text_from_content, match_concepts_to_roadmap
from backend.revision_engine import get_revision_summary
from backend.lesson_content import get_lesson


class TestServerLogicIntegration(unittest.TestCase):

    def setUp(self):
        self.temp_fd, self.temp_path = tempfile.mkstemp(suffix=".db")
        init_db(self.temp_path)

    def tearDown(self):
        os.close(self.temp_fd)
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)

    def test_complete_learning_journey_progression(self):
        # 1. Starting state: recommend Stage 1 foundation
        p1 = get_all_progress(self.temp_path)
        r1 = recommend_next_topic(p1)
        self.assertEqual(r1["recommended_topic"]["id"], "py_syntax")

        # 2. Master py_syntax
        update_topic_progress(
            topic_id="py_syntax",
            status="mastered",
            confidence_rating=5,
            evidence_type="user_confirmed",
            evidence_ref="Completed syntax tutorial",
            db_path=self.temp_path
        )

        # 3. Next recommendation must update to py_operators
        p2 = get_all_progress(self.temp_path)
        r2 = recommend_next_topic(p2)
        self.assertEqual(r2["recommended_topic"]["id"], "py_operators")
        self.assertEqual(len(r2["satisfied_prerequisites"]), 1)
        self.assertEqual(r2["satisfied_prerequisites"][0]["id"], "py_syntax")

        # 4. Master py_operators
        update_topic_progress(
            topic_id="py_operators",
            status="mastered",
            confidence_rating=5,
            db_path=self.temp_path
        )

        # 5. Next recommendation must advance to py_loops
        p3 = get_all_progress(self.temp_path)
        r3 = recommend_next_topic(p3)
        self.assertEqual(r3["recommended_topic"]["id"], "py_loops")

    def test_structured_lesson_completeness(self):
        # Test custom lesson
        l_syntax = get_lesson("py_syntax")
        self.assertIn("lesson", l_syntax)
        lesson_data = l_syntax["lesson"]
        self.assertIn("part1_simple_explanation", lesson_data)
        self.assertIn("part2_analogy", lesson_data)
        self.assertIn("part3_visual_diagram", lesson_data)
        self.assertIn("part4_mechanism", lesson_data)
        self.assertIn("part5_code", lesson_data)
        self.assertIn("part6_when_to_use", lesson_data)
        self.assertIn("part7_problems_engineers_face", lesson_data)
        self.assertIn("part8_knowledge_check", lesson_data)

        # Test dynamic fallback lesson builder for any other topic
        l_any = get_lesson("rag_vector_db")
        self.assertIn("lesson", l_any)
        self.assertIn("part1_simple_explanation", l_any["lesson"])
        self.assertIn("part3_visual_diagram", l_any["lesson"])

    def test_upload_matching_and_confirmation(self):
        sample_doc = """
        Today we worked on Convolutional Neural Networks (CNNs) with max pooling and strides.
        We also covered Python loops and functions.
        """
        p = get_all_progress(self.temp_path)
        analysis = match_concepts_to_roadmap(sample_doc, p["topics_progress"])
        
        found_ids = [item["topic_id"] for item in analysis["group_a_found"]]
        self.assertIn("snn_cnn", found_ids)
        self.assertIn("py_loops", found_ids)

        # User confirms py_loops
        update_topic_progress(
            topic_id="py_loops",
            status="in_progress",
            confidence_rating=3,
            evidence_type="notes_found",
            evidence_ref="Upload confirmation",
            db_path=self.temp_path
        )

        p_after = get_all_progress(self.temp_path)
        self.assertEqual(p_after["topics_progress"]["py_loops"]["status"], "in_progress")


if __name__ == "__main__":
    unittest.main()

