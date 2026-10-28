"""
AI Engineer Learning OS - Database Engine & Persistent Storage
SQLite3-based persistent storage for user learning progress, topic statuses,
evidence logs, quiz attempts, projects, and study uploads.
"""

import sqlite3
import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

from backend.roadmap_data import TOPICS, STAGES

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "learning_os.db")

VALID_STATUSES = {"not_started", "in_progress", "needs_revision", "mastered"}
VALID_EVIDENCE_TYPES = {
    "notes_found",
    "lesson_explained",
    "user_confirmed",
    "practice_completed",
    "quiz_passed",
    "project_completed",
    "mastery_confirmed"
}


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: str = DB_PATH) -> None:
    """Initialize database tables and seed roadmap topics if not present."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # Schema Version table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schema_version (
        version INTEGER PRIMARY KEY,
        applied_at TEXT NOT NULL
    )
    """)

    # User Progress table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_progress (
        topic_id TEXT PRIMARY KEY,
        status TEXT NOT NULL DEFAULT 'not_started',
        confidence_rating INTEGER NOT NULL DEFAULT 1,
        last_studied_date TEXT,
        next_review_date TEXT,
        personal_notes TEXT NOT NULL DEFAULT '',
        updated_at TEXT NOT NULL
    )
    """)

    # Evidence Log table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evidence_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_id TEXT NOT NULL,
        evidence_type TEXT NOT NULL,
        source_ref TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    # Quiz Attempts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_id TEXT NOT NULL,
        score INTEGER NOT NULL,
        total_questions INTEGER NOT NULL,
        passed INTEGER NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    # Projects Progress table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS project_progress (
        project_id TEXT PRIMARY KEY,
        status TEXT NOT NULL DEFAULT 'not_started',
        github_url TEXT NOT NULL DEFAULT '',
        notes TEXT NOT NULL DEFAULT '',
        completed_at TEXT
    )
    """)

    # Uploads history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_uploads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        file_type TEXT NOT NULL,
        file_size INTEGER NOT NULL,
        extracted_text TEXT NOT NULL,
        matched_topics_json TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    # Populate default progress records for all topics
    now_iso = datetime.now(timezone.utc).isoformat()
    for topic in TOPICS:
        cursor.execute("""
        INSERT OR IGNORE INTO user_progress 
        (topic_id, status, confidence_rating, last_studied_date, next_review_date, personal_notes, updated_at)
        VALUES (?, 'not_started', 1, NULL, NULL, '', ?)
        """, (topic["id"], now_iso))

    cursor.execute("INSERT OR IGNORE INTO schema_version (version, applied_at) VALUES (1, ?)", (now_iso,))
    conn.commit()
    conn.close()


def get_all_progress(db_path: str = DB_PATH) -> Dict[str, Any]:
    """Retrieve all user progress mapped by topic_id along with evidence and overall metrics."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_progress")
    progress_rows = cursor.fetchall()
    progress_map = {}
    for row in progress_rows:
        progress_map[row["topic_id"]] = {
            "topic_id": row["topic_id"],
            "status": row["status"],
            "confidence_rating": row["confidence_rating"],
            "last_studied_date": row["last_studied_date"],
            "next_review_date": row["next_review_date"],
            "personal_notes": row["personal_notes"],
            "updated_at": row["updated_at"],
            "evidence": []
        }

    # Fetch evidence items
    cursor.execute("SELECT * FROM evidence_log ORDER BY id DESC")
    evidence_rows = cursor.fetchall()
    for ev in evidence_rows:
        tid = ev["topic_id"]
        if tid in progress_map:
            progress_map[tid]["evidence"].append({
                "id": ev["id"],
                "type": ev["evidence_type"],
                "source_ref": ev["source_ref"],
                "created_at": ev["created_at"]
            })

    # Fetch quiz attempts count
    cursor.execute("SELECT topic_id, score, total_questions, passed, created_at FROM quiz_attempts ORDER BY id DESC")
    quiz_rows = cursor.fetchall()
    quiz_history: Dict[str, List[Dict[str, Any]]] = {}
    for q in quiz_rows:
        tid = q["topic_id"]
        if tid not in quiz_history:
            quiz_history[tid] = []
        quiz_history[tid].append({
            "score": q["score"],
            "total_questions": q["total_questions"],
            "passed": bool(q["passed"]),
            "created_at": q["created_at"]
        })

    # Calculate real-time stats
    total_topics = len(TOPICS)
    mastered = sum(1 for p in progress_map.values() if p["status"] == "mastered")
    in_progress = sum(1 for p in progress_map.values() if p["status"] == "in_progress")
    needs_revision = sum(1 for p in progress_map.values() if p["status"] == "needs_revision")
    not_started = sum(1 for p in progress_map.values() if p["status"] == "not_started")
    completion_percentage = round((mastered / total_topics * 100), 1) if total_topics > 0 else 0.0

    # Find last studied topic
    cursor.execute("SELECT topic_id FROM user_progress WHERE last_studied_date IS NOT NULL ORDER BY last_studied_date DESC LIMIT 1")
    last_studied_row = cursor.fetchone()
    last_studied_id = last_studied_row["topic_id"] if last_studied_row else None

    # Fetch project progress
    cursor.execute("SELECT * FROM project_progress")
    project_rows = cursor.fetchall()
    project_map = {row["project_id"]: dict(row) for row in project_rows}

    conn.close()

    return {
        "topics_progress": progress_map,
        "quiz_history": quiz_history,
        "project_progress": project_map,
        "stats": {
            "total_topics": total_topics,
            "mastered": mastered,
            "in_progress": in_progress,
            "needs_revision": needs_revision,
            "not_started": not_started,
            "completion_percentage": completion_percentage,
            "last_studied_id": last_studied_id
        }
    }


def update_topic_progress(
    topic_id: str,
    status: Optional[str] = None,
    confidence_rating: Optional[int] = None,
    personal_notes: Optional[str] = None,
    mark_studied_now: bool = False,
    next_review_date: Optional[str] = None,
    evidence_type: Optional[str] = None,
    evidence_ref: Optional[str] = None,
    db_path: str = DB_PATH
) -> Dict[str, Any]:
    """Updates learning progress for a specific topic with audit evidence."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    now_iso = datetime.now(timezone.utc).isoformat()

    cursor.execute("SELECT * FROM user_progress WHERE topic_id = ?", (topic_id,))
    existing = cursor.fetchone()
    if not existing:
        conn.close()
        raise ValueError(f"Topic ID {topic_id} does not exist in roadmap.")

    current_status = status if status in VALID_STATUSES else existing["status"]
    current_confidence = confidence_rating if confidence_rating is not None and 1 <= confidence_rating <= 5 else existing["confidence_rating"]
    current_notes = personal_notes if personal_notes is not None else existing["personal_notes"]
    current_last_studied = now_iso if mark_studied_now else existing["last_studied_date"]
    current_next_review = next_review_date if next_review_date is not None else existing["next_review_date"]

    cursor.execute("""
    UPDATE user_progress
    SET status = ?, confidence_rating = ?, personal_notes = ?, last_studied_date = ?, next_review_date = ?, updated_at = ?
    WHERE topic_id = ?
    """, (current_status, current_confidence, current_notes, current_last_studied, current_next_review, now_iso, topic_id))

    if evidence_type and evidence_type in VALID_EVIDENCE_TYPES:
        cursor.execute("""
        INSERT INTO evidence_log (topic_id, evidence_type, source_ref, created_at)
        VALUES (?, ?, ?, ?)
        """, (topic_id, evidence_type, evidence_ref or "Manual user action", now_iso))

    conn.commit()
    conn.close()

    return {
        "topic_id": topic_id,
        "status": current_status,
        "confidence_rating": current_confidence,
        "last_studied_date": current_last_studied,
        "next_review_date": current_next_review,
        "personal_notes": current_notes,
        "updated_at": now_iso
    }


def record_quiz_attempt(
    topic_id: str,
    score: int,
    total_questions: int,
    db_path: str = DB_PATH
) -> Dict[str, Any]:
    """Record a completed quiz attempt and log evidence."""
    passed = 1 if (score / total_questions) >= 0.70 else 0
    now_iso = datetime.now(timezone.utc).isoformat()
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO quiz_attempts (topic_id, score, total_questions, passed, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (topic_id, score, total_questions, passed, now_iso))

    # Add evidence
    evidence_desc = f"Quiz: {score}/{total_questions} ({'Passed' if passed else 'Failed'})"
    evidence_type = "quiz_passed" if passed else "practice_completed"
    cursor.execute("""
    INSERT INTO evidence_log (topic_id, evidence_type, source_ref, created_at)
    VALUES (?, ?, ?, ?)
    """, (topic_id, evidence_type, evidence_desc, now_iso))

    # Update status: if passed and currently not_started or needs_revision, set to in_progress or mastered based on evidence
    cursor.execute("SELECT status, confidence_rating FROM user_progress WHERE topic_id = ?", (topic_id,))
    row = cursor.fetchone()
    if row:
        new_status = row["status"]
        if passed:
            if row["status"] in ("not_started", "needs_revision"):
                new_status = "in_progress"
            new_conf = min(5, row["confidence_rating"] + 1)
        else:
            new_conf = max(1, row["confidence_rating"] - 1)
            new_status = "needs_revision"

        cursor.execute("""
        UPDATE user_progress 
        SET status = ?, confidence_rating = ?, last_studied_date = ?, updated_at = ?
        WHERE topic_id = ?
        """, (new_status, new_conf, now_iso, now_iso, topic_id))

    conn.commit()
    conn.close()

    return {
        "topic_id": topic_id,
        "score": score,
        "total_questions": total_questions,
        "passed": bool(passed),
        "recorded_at": now_iso
    }


def record_project_progress(
    project_id: str,
    status: str,
    github_url: str = "",
    notes: str = "",
    db_path: str = DB_PATH
) -> Dict[str, Any]:
    """Records practical project completion and updates topic evidence."""
    now_iso = datetime.now(timezone.utc).isoformat()
    completed_at = now_iso if status == "completed" else None
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO project_progress (project_id, status, github_url, notes, completed_at)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(project_id) DO UPDATE SET
        status = excluded.status,
        github_url = excluded.github_url,
        notes = excluded.notes,
        completed_at = excluded.completed_at
    """, (project_id, status, github_url, notes, completed_at))

    # Find associated topics from STAGES practical_projects to log evidence
    for stage in STAGES:
        for proj in stage.get("practical_projects", []):
            if proj["id"] == project_id and status == "completed":
                for prereq_tid in proj.get("prerequisites", []):
                    cursor.execute("""
                    INSERT INTO evidence_log (topic_id, evidence_type, source_ref, created_at)
                    VALUES (?, 'project_completed', ?, ?)
                    """, (prereq_tid, f"Completed project: {proj['title']}", now_iso))

    conn.commit()
    conn.close()

    return {
        "project_id": project_id,
        "status": status,
        "github_url": github_url,
        "notes": notes,
        "completed_at": completed_at
    }


def record_upload(
    filename: str,
    file_type: str,
    file_size: int,
    extracted_text: str,
    matched_topics: List[Dict[str, Any]],
    db_path: str = DB_PATH
) -> int:
    """Save an upload record and its extracted metadata."""
    now_iso = datetime.now(timezone.utc).isoformat()
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO study_uploads (filename, file_type, file_size, extracted_text, matched_topics_json, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (filename, file_type, file_size, extracted_text, json.dumps(matched_topics), now_iso))

    upload_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return upload_id


def export_database_json(db_path: str = DB_PATH) -> Dict[str, Any]:
    """Full export of user progress, evidence, quizzes, and project data."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_progress")
    progress = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM evidence_log")
    evidence = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM quiz_attempts")
    quizzes = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM project_progress")
    projects = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, filename, file_type, file_size, created_at FROM study_uploads")
    uploads = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "app": "AI Engineer Learning OS",
        "schema_version": 1,
        "user_progress": progress,
        "evidence_log": evidence,
        "quiz_attempts": quizzes,
        "project_progress": projects,
        "study_uploads": uploads
    }


def import_database_json(data: Dict[str, Any], db_path: str = DB_PATH) -> Dict[str, Any]:
    """Validate and restore user progress from an exported JSON object."""
    if not isinstance(data, dict) or "user_progress" not in data:
        raise ValueError("Invalid import payload: missing user_progress data.")

    conn = get_connection(db_path)
    cursor = conn.cursor()
    imported_topics = 0

    for item in data.get("user_progress", []):
        tid = item.get("topic_id")
        if not tid:
            continue
        status = item.get("status", "not_started")
        if status not in VALID_STATUSES:
            status = "not_started"
        confidence = int(item.get("confidence_rating", 1))
        notes = item.get("personal_notes", "")
        last_studied = item.get("last_studied_date")
        next_review = item.get("next_review_date")
        updated_at = item.get("updated_at", datetime.now(timezone.utc).isoformat())

        cursor.execute("""
        INSERT INTO user_progress (topic_id, status, confidence_rating, last_studied_date, next_review_date, personal_notes, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(topic_id) DO UPDATE SET
            status = excluded.status,
            confidence_rating = excluded.confidence_rating,
            last_studied_date = excluded.last_studied_date,
            next_review_date = excluded.next_review_date,
            personal_notes = excluded.personal_notes,
            updated_at = excluded.updated_at
        """, (tid, status, confidence, last_studied, next_review, notes, updated_at))
        imported_topics += 1

    conn.commit()
    conn.close()

    return {
        "success": True,
        "imported_topics": imported_topics,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


def reset_learning_data(db_path: str = DB_PATH) -> None:
    """Reset all user learning progress back to clean initial state."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM evidence_log")
    cursor.execute("DELETE FROM quiz_attempts")
    cursor.execute("DELETE FROM project_progress")
    cursor.execute("DELETE FROM study_uploads")
    
    now_iso = datetime.now(timezone.utc).isoformat()
    cursor.execute("""
    UPDATE user_progress 
    SET status = 'not_started', confidence_rating = 1, last_studied_date = NULL, next_review_date = NULL, personal_notes = '', updated_at = ?
    """, (now_iso,))

    conn.commit()
    conn.close()
