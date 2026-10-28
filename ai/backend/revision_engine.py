"""
AI Engineer Learning OS - Spaced Repetition & Revision Engine
Transparent review scheduling based on user confidence, quiz results,
and spaced intervals (1d, 3d, 7d, 14d, 30d).
"""

from typing import Dict, Any, List
from datetime import datetime, timezone, timedelta
from backend.roadmap_data import TOPICS, STAGES, get_topic_by_id


# Interval intervals mapped to confidence levels
INTERVAL_DAYS = {
    1: 1,    # Shaky / just started: 1 day
    2: 3,    # Beginner grasp: 3 days
    3: 7,    # Good working knowledge: 1 week
    4: 14,   # Solid retention: 2 weeks
    5: 30    # Mastered / deeply internalized: 1 month
}


def compute_next_review_date(confidence: int, passed_quiz: bool = True) -> str:
    """Calculate the next ISO review timestamp based on confidence and quiz result."""
    now = datetime.now(timezone.utc)
    if not passed_quiz:
        days = 1
    else:
        days = INTERVAL_DAYS.get(confidence, 3)
    return (now + timedelta(days=days)).isoformat()


def get_revision_summary(progress_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes revision queues:
    - Due today
    - Overdue topics
    - Weak concepts (low quiz score or low confidence)
    - Topics marked 'needs_revision'
    - Recently mastered topics
    """
    progress_map = progress_data.get("topics_progress", {})
    quiz_history = progress_data.get("quiz_history", {})
    now = datetime.now(timezone.utc)
    today_date = now.date()

    due_today = []
    overdue = []
    weak_concepts = []
    needs_revision_list = []
    recently_mastered = []

    for topic in TOPICS:
        tid = topic["id"]
        prog = progress_map.get(tid, {})
        status = prog.get("status", "not_started")
        confidence = prog.get("confidence_rating", 1)
        next_review_str = prog.get("next_review_date")
        last_studied_str = prog.get("last_studied_date")

        if status == "not_started":
            continue

        item = {
            "topic_id": tid,
            "title": topic["title"],
            "stage_id": topic["stage_id"],
            "stage_name": STAGES[topic["stage_id"] - 1]["name"],
            "difficulty": topic["difficulty"],
            "status": status,
            "confidence_rating": confidence,
            "next_review_date": next_review_str,
            "last_studied_date": last_studied_str,
            "quiz_attempts": quiz_history.get(tid, [])
        }

        # Check needs_revision
        if status == "needs_revision":
            needs_revision_list.append(item)

        # Check weak concepts (confidence <= 2 or failed quiz)
        quizzes = quiz_history.get(tid, [])
        has_failed_quiz = any(not q["passed"] for q in quizzes)
        if (confidence <= 2 and status != "not_started") or has_failed_quiz:
            weak_item = dict(item)
            weak_item["weak_reason"] = "Failed recent quiz attempt" if has_failed_quiz else f"Low confidence rating ({confidence}/5)"
            weak_concepts.append(weak_item)

        # Check due dates
        if next_review_str:
            try:
                dt = datetime.fromisoformat(next_review_str.replace("Z", "+00:00"))
                review_date = dt.date()
                if review_date < today_date:
                    days_past = (today_date - review_date).days
                    overdue_item = dict(item)
                    overdue_item["days_overdue"] = days_past
                    overdue.append(overdue_item)
                elif review_date == today_date:
                    due_today.append(item)
            except Exception:
                pass

        # Check recently mastered (within last 7 days)
        if status == "mastered" and last_studied_str:
            try:
                ls_dt = datetime.fromisoformat(last_studied_str.replace("Z", "+00:00"))
                if (now - ls_dt).days <= 7:
                    recently_mastered.append(item)
            except Exception:
                pass

    return {
        "due_today": due_today,
        "overdue": overdue,
        "needs_revision": needs_revision_list,
        "weak_concepts": weak_concepts,
        "recently_mastered": recently_mastered,
        "counts": {
            "due_today_count": len(due_today),
            "overdue_count": len(overdue),
            "needs_revision_count": len(needs_revision_list),
            "weak_concepts_count": len(weak_concepts),
            "recently_mastered_count": len(recently_mastered)
        }
    }

