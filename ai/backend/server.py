"""
AI Engineer Learning OS - REST API & Static Web Server
Runs a lightweight, zero-dependency, multithreaded HTTP server
serving the SPA frontend and complete JSON API endpoints.
"""

import http.server
import json
import os
import sys
import urllib.parse
from datetime import datetime, timezone
from typing import Dict, Any, Tuple

from backend.database import (
    init_db,
    get_all_progress,
    update_topic_progress,
    record_quiz_attempt,
    record_project_progress,
    record_upload,
    export_database_json,
    import_database_json,
    reset_learning_data,
    DB_PATH
)
from backend.roadmap_data import STAGES, TOPICS, get_topic_by_id
from backend.recommendation import recommend_next_topic, explain_prerequisite_tree
from backend.upload_parser import extract_text_from_content, match_concepts_to_roadmap
from backend.revision_engine import get_revision_summary, compute_next_review_date
from backend.lesson_content import get_lesson

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")


class LearningOSRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler serving REST API endpoints and static frontend assets."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def end_headers(self) -> None:
        """Injects no-cache headers for all responses so browser always gets fresh assets."""
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def _send_json(self, data: Any, status_code: int = 200) -> None:
        """Sends a JSON response with standard CORS and no-cache headers."""
        payload = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(payload)

    def _read_json_body(self) -> Dict[str, Any]:
        """Reads and parses incoming JSON payload from request body."""
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length == 0:
                return {}
            raw_bytes = self.rfile.read(length)
            return json.loads(raw_bytes.decode("utf-8"))
        except Exception as e:
            return {"_parse_error": str(e)}

    def do_OPTIONS(self) -> None:
        """Handle CORS pre-flight requests."""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_HEAD(self) -> None:
        """Handles HEAD requests identically to GET without writing the response body."""
        self.do_GET()

    def do_GET(self) -> None:
        """Routes GET API endpoints or serves frontend static files."""
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # API Routes
        if path == "/api/health":
            self._send_json({
                "status": "healthy",
                "app": "AI Engineer Learning OS",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "storage": "SQLite3 (Local Persistent)",
                "ai_provider_configured": bool(os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")),
                "ocr_provider_configured": bool(os.getenv("OCR_API_KEY"))
            })
            return

        if path == "/api/roadmap":
            self._send_json({
                "stages": STAGES,
                "topics": TOPICS,
                "total_stages": len(STAGES),
                "total_topics": len(TOPICS)
            })
            return

        if path == "/api/progress":
            progress_data = get_all_progress()
            self._send_json(progress_data)
            return

        if path == "/api/recommendation":
            progress_data = get_all_progress()
            recommendation = recommend_next_topic(progress_data)
            self._send_json(recommendation)
            return

        if path.startswith("/api/topic/"):
            topic_id = path[len("/api/topic/"):]
            topic_id = urllib.parse.unquote(topic_id).split("#")[0].split("?")[0].strip()
            lesson_data = get_lesson(topic_id)
            if "error" in lesson_data:
                self._send_json(lesson_data, status_code=404)
            else:
                self._send_json(lesson_data)
            return

        if path.startswith("/api/prerequisites/"):
            topic_id = path[len("/api/prerequisites/"):]
            progress_data = get_all_progress()
            tree = explain_prerequisite_tree(topic_id, progress_data.get("topics_progress", {}))
            self._send_json(tree)
            return

        if path == "/api/revisions":
            progress_data = get_all_progress()
            revisions = get_revision_summary(progress_data)
            self._send_json(revisions)
            return

        if path == "/api/projects":
            progress_data = get_all_progress()
            all_projects = []
            for st in STAGES:
                for p in st.get("practical_projects", []):
                    item = dict(p)
                    item["stage_id"] = st["id"]
                    item["stage_name"] = st["name"]
                    p_state = progress_data.get("project_progress", {}).get(p["id"], {})
                    item["status"] = p_state.get("status", "not_started")
                    item["github_url"] = p_state.get("github_url", "")
                    item["notes"] = p_state.get("notes", "")
                    item["completed_at"] = p_state.get("completed_at")
                    all_projects.append(item)
            self._send_json({"projects": all_projects})
            return

        if path == "/api/export":
            backup = export_database_json()
            self._send_json(backup)
            return

        # Default static file handler for frontend files
        if path == "/" or not os.path.exists(os.path.join(FRONTEND_DIR, path.lstrip("/"))):
            # SPA fallback: if requesting unknown HTML path, return index.html
            if not path.startswith("/api/"):
                self.path = "/index.html"
        return super().do_GET()

    def do_POST(self) -> None:
        """Handles POST API actions (progress update, quiz submit, upload, import)."""
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == "/api/progress/topic":
            body = self._read_json_body()
            topic_id = body.get("topic_id")
            if not topic_id:
                self._send_json({"error": "Missing topic_id"}, status_code=400)
                return
            try:
                result = update_topic_progress(
                    topic_id=topic_id,
                    status=body.get("status"),
                    confidence_rating=body.get("confidence_rating"),
                    personal_notes=body.get("personal_notes"),
                    mark_studied_now=body.get("mark_studied_now", False),
                    next_review_date=body.get("next_review_date"),
                    evidence_type=body.get("evidence_type"),
                    evidence_ref=body.get("evidence_ref")
                )
                self._send_json(result)
            except Exception as e:
                self._send_json({"error": str(e)}, status_code=400)
            return

        if path == "/api/quiz/submit":
            body = self._read_json_body()
            topic_id = body.get("topic_id")
            score = int(body.get("score", 0))
            total = int(body.get("total_questions", 1))
            if not topic_id:
                self._send_json({"error": "Missing topic_id"}, status_code=400)
                return
            result = record_quiz_attempt(topic_id, score, total)
            self._send_json(result)
            return

        if path == "/api/projects/status":
            body = self._read_json_body()
            project_id = body.get("project_id")
            status = body.get("status", "not_started")
            github_url = body.get("github_url", "")
            notes = body.get("notes", "")
            if not project_id:
                self._send_json({"error": "Missing project_id"}, status_code=400)
                return
            res = record_project_progress(project_id, status, github_url, notes)
            self._send_json(res)
            return

        if path == "/api/upload":
            # Supports JSON payload with file_content or raw file text
            body = self._read_json_body()
            filename = body.get("filename", "notes.txt")
            raw_text = body.get("text_content", "")
            
            # If text provided directly
            if not raw_text and "base64_content" in body:
                import base64
                content_bytes = base64.b64decode(body["base64_content"])
                extracted_text, parser_type, diagnostics = extract_text_from_content(content_bytes, filename)
            elif raw_text:
                extracted_text = raw_text
                parser_type = "direct_text"
                diagnostics = {"size": len(raw_text)}
            else:
                self._send_json({"error": "No file content or text provided"}, status_code=400)
                return

            progress_data = get_all_progress()
            matched = match_concepts_to_roadmap(extracted_text, progress_data.get("topics_progress", {}))

            upload_id = record_upload(
                filename=filename,
                file_type=parser_type,
                file_size=len(extracted_text),
                extracted_text=extracted_text[:2000],  # store preview
                matched_topics=matched["group_a_found"]
            )

            self._send_json({
                "upload_id": upload_id,
                "filename": filename,
                "parser_type": parser_type,
                "diagnostics": diagnostics,
                "analysis": matched
            })
            return

        if path == "/api/upload/confirm":
            body = self._read_json_body()
            confirmed_topics = body.get("confirmed_topics", [])
            upload_id = body.get("upload_id")
            filename = body.get("filename", "Uploaded Material")

            updated_count = 0
            for item in confirmed_topics:
                tid = item.get("topic_id")
                new_status = item.get("status", "in_progress")
                confidence = int(item.get("confidence", 2))
                update_topic_progress(
                    topic_id=tid,
                    status=new_status,
                    confidence_rating=confidence,
                    evidence_type="notes_found",
                    evidence_ref=f"Extracted from {filename} (Upload #{upload_id})"
                )
                updated_count += 1

            self._send_json({
                "success": True,
                "updated_count": updated_count,
                "message": f"Successfully updated learning progress for {updated_count} topics."
            })
            return

        if path == "/api/import":
            body = self._read_json_body()
            try:
                res = import_database_json(body)
                self._send_json(res)
            except Exception as e:
                self._send_json({"error": str(e)}, status_code=400)
            return

        if path == "/api/reset":
            reset_learning_data()
            self._send_json({"success": True, "message": "All learning progress has been reset to initial state."})
            return

        self._send_json({"error": f"Unknown POST endpoint: {path}"}, status_code=404)


def run_server(port: int = 8000, bind_address: str = "0.0.0.0") -> None:
    """Initializes the database and starts the multithreaded HTTP server."""
    init_db()
    server_address = (bind_address, port)
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    httpd = http.server.ThreadingHTTPServer(server_address, LearningOSRequestHandler)
    print(f"============================================================")
    print(f"  AI Engineer Learning OS Server Started")
    print(f"  URL: http://{bind_address}:{port}")
    print(f"  Database: {DB_PATH}")
    print(f"  Frontend: {FRONTEND_DIR}")
    print(f"============================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server gracefully...")
        httpd.server_close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port=port)

