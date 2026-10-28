"""
AI Engineer Learning OS - Intelligent Recommendation Engine
Prerequisite-aware topological graph engine that recommends the optimal next topic
based on completed prerequisites, confidence, revision needs, and foundational stages.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from backend.roadmap_data import TOPICS, STAGES, get_topic_by_id


def is_prerequisite_satisfied(prereq_id: str, progress_map: Dict[str, Any]) -> bool:
    """A prerequisite is considered satisfied if it is marked as 'mastered' or 'in_progress' with confidence >= 3."""
    user_p = progress_map.get(prereq_id)
    if not user_p:
        return False
    status = user_p.get("status")
    confidence = user_p.get("confidence_rating", 1)
    if status == "mastered":
        return True
    if status == "in_progress" and confidence >= 3:
        return True
    return False


def get_topic_unlocked_count(topic_id: str) -> int:
    """Calculate how many downstream topics directly list this topic as a prerequisite."""
    count = 0
    for t in TOPICS:
        if topic_id in t.get("prerequisites", []):
            count += 1
    return count


def recommend_next_topic(progress_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Selects the single optimal next topic based on:
    1. Prerequisite completion (strictly enforces that all prerequisites are satisfied).
    2. Needs revision prioritization for shaky concepts.
    3. Earliest foundation stages prioritized (Stage 1 -> 2 -> 3...).
    4. Topological leverage (topics that unlock more downstream concepts).
    5. Detailed reason explanation & satisfied prerequisite breakdown.
    """
    progress_map = progress_data.get("topics_progress", {})

    # Check for urgent revision needs
    revision_candidates = []
    for t in TOPICS:
        tid = t["id"]
        p = progress_map.get(tid, {})
        status = p.get("status", "not_started")
        confidence = p.get("confidence_rating", 1)
        next_review = p.get("next_review_date")
        
        # Check if due for revision
        is_overdue = False
        if next_review:
            try:
                dt = datetime.fromisoformat(next_review.replace("Z", "+00:00"))
                is_overdue = dt <= datetime.now(timezone.utc)
            except Exception:
                pass

        if status == "needs_revision" or is_overdue or (status == "in_progress" and confidence == 1 and p.get("last_studied_date")):
            # All its prerequisites must still be satisfied
            prereqs_ok = all(is_prerequisite_satisfied(pre, progress_map) for pre in t.get("prerequisites", []))
            if prereqs_ok:
                revision_candidates.append((t, p, "revision"))

    # Eligible uncompleted topics where all prerequisites are satisfied
    ready_candidates = []
    blocked_candidates = []

    for t in TOPICS:
        tid = t["id"]
        p = progress_map.get(tid, {})
        status = p.get("status", "not_started")

        if status == "mastered":
            continue

        prereqs = t.get("prerequisites", [])
        satisfied_prereqs = [pre for pre in prereqs if is_prerequisite_satisfied(pre, progress_map)]
        missing_prereqs = [pre for pre in prereqs if not is_prerequisite_satisfied(pre, progress_map)]

        if len(missing_prereqs) == 0:
            # Score this candidate:
            # - Lower stage_id is preferred (foundations first)
            # - In progress topics get a boost to finish what was started
            # - More downstream unlocks get higher priority
            stage_penalty = t["stage_id"] * 100
            in_progress_bonus = -50 if status == "in_progress" else 0
            unlocks_bonus = - (get_topic_unlocked_count(tid) * 10)
            score = stage_penalty + in_progress_bonus + unlocks_bonus
            ready_candidates.append({
                "topic": t,
                "progress": p,
                "score": score,
                "satisfied_prereqs": satisfied_prereqs,
                "missing_prereqs": missing_prereqs
            })
        else:
            blocked_candidates.append({
                "topic": t,
                "progress": p,
                "satisfied_prereqs": satisfied_prereqs,
                "missing_prereqs": missing_prereqs
            })

    # Sort ready candidates by priority score ascending (lowest score = highest priority)
    ready_candidates.sort(key=lambda x: x["score"])

    # If there are revision candidates that urgently need reinforcement
    selected_topic = None
    selection_reason = ""
    suggested_practice = ""
    alternatives = []

    if revision_candidates:
        rev_t, rev_p, _ = revision_candidates[0]
        selected_topic = rev_t
        selection_reason = (
            f"Reinforcement Required: You previously studied '{rev_t['title']}', but it is marked for revision "
            f"or has low confidence ({rev_p.get('confidence_rating', 1)}/5). Revising this now guarantees that "
            f"downstream concepts in Stage {rev_t['stage_id']} rest on a rock-solid foundation."
        )
        suggested_practice = f"Complete a 5-question refresher quiz on {rev_t['title']} and inspect the step-by-step visual diagram."
        
        # Add a couple of other ready topics as alternatives
        for cand in ready_candidates[:2]:
            alternatives.append({
                "id": cand["topic"]["id"],
                "title": cand["topic"]["title"],
                "stage_id": cand["topic"]["stage_id"],
                "reason": f"Ready to start new content in Stage {cand['topic']['stage_id']} if you prefer to continue advancing."
            })

    elif ready_candidates:
        best = ready_candidates[0]
        selected_topic = best["topic"]
        sat_names = [get_topic_by_id(pid)["title"] for pid in best["satisfied_prereqs"] if get_topic_by_id(pid)]

        if not sat_names:
            selection_reason = (
                f"Essential Foundation: '{selected_topic['title']}' has no prerequisites and is the foundational entry point "
                f"for Stage {selected_topic['stage_id']} ({STAGES[selected_topic['stage_id']-1]['name']}). Starting here ensures you build correct habits from Day 1."
            )
        else:
            prereq_str = ", ".join(sat_names)
            selection_reason = (
                f"Prerequisites Completed: You have successfully satisfied the required foundations ({prereq_str}). "
                f"Learning '{selected_topic['title']}' is the logical next step in Stage {selected_topic['stage_id']}, "
                f"which directly prepares you for {get_topic_unlocked_count(selected_topic['id'])} downstream AI engineering topics."
            )

        suggested_practice = f"Implement a mini-exercise practicing {selected_topic['key_concepts'][0]} and {selected_topic['key_concepts'][1]}."

        # Provide up to 2 alternative choices with rationale
        for cand in ready_candidates[1:3]:
            cand_t = cand["topic"]
            alternatives.append({
                "id": cand_t["id"],
                "title": cand_t["title"],
                "stage_id": cand_t["stage_id"],
                "difficulty": cand_t["difficulty"],
                "reason": f"Also ready: All prerequisites satisfied in Stage {cand_t['stage_id']}. Ideal if you want to branch into {cand_t['title']}."
            })

    else:
        # All topics mastered!
        selected_topic = TOPICS[0]
        selection_reason = "Congratulations! You have mastered all topics across all 12 stages in the AI Engineering roadmap."
        suggested_practice = "Review your portfolio projects and deploy an end-to-end production LLM agent."

    # Build downstream unlocked topics
    downstream = []
    for t in TOPICS:
        if selected_topic["id"] in t.get("prerequisites", []):
            downstream.append({
                "id": t["id"],
                "title": t["title"],
                "stage_id": t["stage_id"]
            })

    # Build detailed satisfied prerequisite objects
    satisfied_details = []
    for pid in selected_topic.get("prerequisites", []):
        pt = get_topic_by_id(pid)
        if pt:
            p_prog = progress_map.get(pid, {})
            satisfied_details.append({
                "id": pid,
                "title": pt["title"],
                "stage_id": pt["stage_id"],
                "status": p_prog.get("status", "not_started"),
                "confidence": p_prog.get("confidence_rating", 1)
            })

    return {
        "recommended_topic": {
            "id": selected_topic["id"],
            "stage_id": selected_topic["stage_id"],
            "stage_name": STAGES[selected_topic["stage_id"] - 1]["name"],
            "title": selected_topic["title"],
            "difficulty": selected_topic["difficulty"],
            "estimated_hours": selected_topic["estimated_hours"],
            "importance": selected_topic["importance"],
            "what_you_will_do": selected_topic["what_you_will_do"],
            "key_concepts": selected_topic["key_concepts"],
            "status": progress_map.get(selected_topic["id"], {}).get("status", "not_started"),
            "confidence_rating": progress_map.get(selected_topic["id"], {}).get("confidence_rating", 1)
        },
        "reason": selection_reason,
        "suggested_practice": suggested_practice,
        "satisfied_prerequisites": satisfied_details,
        "downstream_unlocked": downstream,
        "alternative_choices": alternatives,
        "has_pending_prerequisites": False
    }


def explain_prerequisite_tree(topic_id: str, progress_map: Dict[str, Any]) -> Dict[str, Any]:
    """Generates a complete prerequisite chain inspection for a specific topic."""
    target = get_topic_by_id(topic_id)
    if not target:
        return {"error": "Topic not found"}

    chain = []
    to_visit = list(target.get("prerequisites", []))
    visited = set()

    while to_visit:
        curr_id = to_visit.pop(0)
        if curr_id in visited:
            continue
        visited.add(curr_id)
        pt = get_topic_by_id(curr_id)
        if pt:
            prog = progress_map.get(curr_id, {})
            is_sat = is_prerequisite_satisfied(curr_id, progress_map)
            chain.append({
                "id": curr_id,
                "title": pt["title"],
                "stage_id": pt["stage_id"],
                "stage_name": STAGES[pt["stage_id"] - 1]["name"],
                "status": prog.get("status", "not_started"),
                "confidence": prog.get("confidence_rating", 1),
                "is_satisfied": is_sat
            })
            for p in pt.get("prerequisites", []):
                if p not in visited:
                    to_visit.append(p)

    return {
        "target_topic": {
            "id": target["id"],
            "title": target["title"],
            "stage_id": target["stage_id"]
        },
        "prerequisites_chain": chain,
        "all_satisfied": all(item["is_satisfied"] for item in chain)
    }

