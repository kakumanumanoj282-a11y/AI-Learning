"""
Unit tests for AI Engineer Learning OS Database Engine & Persistence.
"""

import unittest
import os
import tempfile
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
from backend.roadmap_data import TOPICS


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        init_db(self.temp_db_path)

    def tearDown(self):
        os.close(self.temp_db_fd)
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def test_database_initialization(self):
        data = get_all_progress(self.temp_db_path)
        self.assertEqual(len(data["topics_progress"]), len(TOPICS))
        self.assertEqual(data["stats"]["mastered"], 0)
        self.assertEqual(data["stats"]["not_started"], len(TOPICS))
        self.assertEqual(data["stats"]["completion_percentage"], 0.0)

    def test_topic_progress_update_and_evidence(self):
        topic_id = "py_syntax"
        res = update_topic_progress(
            topic_id=topic_id,
            status="mastered",
            confidence_rating=5,
            personal_notes="Completed deep study of variables and syntax",
            mark_studied_now=True,
            evidence_type="user_confirmed",
            evidence_ref="Self-assessment verified",
            db_path=self.temp_db_path
        )
        self.assertEqual(res["status"], "mastered")
        self.assertEqual(res["confidence_rating"], 5)

        data = get_all_progress(self.temp_db_path)
        p = data["topics_progress"][topic_id]
        self.assertEqual(p["status"], "mastered")
        self.assertEqual(p["confidence_rating"], 5)
        self.assertEqual(len(p["evidence"]), 1)
        self.assertEqual(p["evidence"][0]["type"], "user_confirmed")
        self.assertEqual(data["stats"]["mastered"], 1)

    def test_quiz_attempt_recording(self):
        topic_id = "math_dot_products"
        # Passing quiz (score 3/3 -> 100%)
        q_res = record_quiz_attempt(topic_id, score=3, total_questions=3, db_path=self.temp_db_path)
        self.assertTrue(q_res["passed"])

        data = get_all_progress(self.temp_db_path)
        p = data["topics_progress"][topic_id]
        self.assertEqual(p["status"], "in_progress")
        self.assertGreaterEqual(p["confidence_rating"], 2)
        self.assertIn(topic_id, data["quiz_history"])

        # Failing quiz -> should set to needs_revision
        record_quiz_attempt(topic_id, score=1, total_questions=3, db_path=self.temp_db_path)
        data2 = get_all_progress(self.temp_db_path)
        p2 = data2["topics_progress"][topic_id]
        self.assertEqual(p2["status"], "needs_revision")

    def test_project_progress_recording(self):
        proj_id = "proj_1_calc"
        res = record_project_progress(
            project_id=proj_id,
            status="completed",
            github_url="https://github.com/user/calc",
            notes="Implemented custom CLI calculator with unit tests",
            db_path=self.temp_db_path
        )
        self.assertEqual(res["status"], "completed")

        data = get_all_progress(self.temp_db_path)
        self.assertIn(proj_id, data["project_progress"])
        self.assertEqual(data["project_progress"][proj_id]["status"], "completed")

    def test_export_and_import(self):
        # Update something
        update_topic_progress(
            topic_id="py_syntax",
            status="mastered",
            confidence_rating=4,
            db_path=self.temp_db_path
        )
        backup = export_database_json(self.temp_db_path)
        self.assertIn("user_progress", backup)
        self.assertGreater(len(backup["user_progress"]), 0)

        # Reset and verify empty
        reset_learning_data(self.temp_db_path)
        data_reset = get_all_progress(self.temp_db_path)
        self.assertEqual(data_reset["stats"]["mastered"], 0)

        # Restore from backup
        import_res = import_database_json(backup, self.temp_db_path)
        self.assertTrue(import_res["success"])

        data_restored = get_all_progress(self.temp_db_path)
        self.assertEqual(data_restored["topics_progress"]["py_syntax"]["status"], "mastered")


if __name__ == "__main__":
    unittest.main()

