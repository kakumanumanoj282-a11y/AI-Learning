# AI Engineer Learning OS

A personal, production-minded learning management system and developer dashboard designed for aspiring AI Engineers.

---

## 1. System Overview

The **AI Engineer Learning OS** helps beginners master advanced AI topics through structured, prerequisite-aware roadmaps, visual mental models, code demonstrations, problem-solving playbooks, and self-assessment checks.

The application answers the five core learning questions:
1. **What have I already learned?** — Real computed statistics from SQLite audit evidence.
2. **What topics are still pending?** — Filterable queue of upcoming roadmap concepts.
3. **What should I learn next?** — Prerequisite-aware topological recommendation engine.
4. **Why should I learn that topic and what prerequisites do I need?** — Transparent justification with prerequisite trees and downstream unlock lists.
5. **Can I understand the topic through diagrams, examples, and small projects?** — Structured 9-part lessons with interactive SVG diagrams, runnable Python code, and practical exercises.

---

## 2. 12-Stage AI Engineering Curriculum

1. **Stage 1: Programming Foundations** — Python syntax, variables, data structures, OOP, Git, terminal tools.
2. **Stage 2: Mathematics for AI** — Vectors, matrices, dot products, derivatives, gradients, chain rule, optimization.
3. **Stage 3: Data Analysis and Processing** — NumPy, Pandas, data cleaning, feature scaling, data leakage prevention, SQL.
4. **Stage 4: Machine Learning** — Linear regression, logistic regression, decision trees, random forests, gradient boosting, evaluation metrics.
5. **Stage 5: Deep Learning** — Artificial neurons, forward/backward propagation, activation functions, optimizers, PyTorch fundamentals.
6. **Stage 6: Specialized Neural Networks** — CNNs, RNNs, Attention mechanisms, the Transformer architecture, Query-Key-Value matrices.
7. **Stage 7: Natural Language Processing & LLMs** — Tokenization, context windows, prompt engineering, structured JSON outputs, streaming.
8. **Stage 8: Retrieval-Augmented Generation (RAG)** — Chunking, vector embeddings, vector databases (HNSW), hybrid search, reranking, source citations.
9. **Stage 9: AI Agents and Tool Use** — ReAct loop, tool calling, memory systems, task decomposition, human-in-the-loop approval.
10. **Stage 10: Backend and AI Application Development** — FastAPI, Pydantic, async I/O, Docker containerization.
11. **Stage 11: AI Deployment and MLOps** — Model serving (ONNX/vLLM), data drift detection, latency monitoring, cost observability.
12. **Stage 12: Advanced AI Engineering** — PEFT / LoRA fine-tuning, GPU VRAM optimization, LLM evaluations, prompt injection defenses.

---

## 3. Architecture & Technical Choices

- **Frontend:** Responsive, native ES6 Single Page Application (SPA) with dark developer aesthetic (`#080c14` near-black, electric blue, royal violet, cyan accents), interactive SVG dataflow diagrams, and light/dark theme toggle. Zero build step required.
- **Backend:** Python 3.10+ multithreaded HTTP REST server (`ThreadingHTTPServer`) with zero external pip dependencies.
- **Database Engine:** Embedded SQLite3 database with schema versioning, audit evidence logging, quiz tracking, and JSON backup export/import.
- **Recommendation Engine:** Topological prerequisite graph traversal that prioritizes foundational stages, prevents skipping essential prerequisites, and prioritizes shaky or revision-due concepts.
- **Study Notes Analyzer:** Extracts keywords and formulas from notes, code files, and documents, categorizing matches into:
  - **Group A:** Topics found in the uploaded material.
  - **Group B:** Topics already recorded as learned.
  - **Group C:** Missing prerequisites requiring further study.
  - Displays a confirmation review screen before modifying user progress.

---

## 4. Setup & Quickstart

### Prerequisites
- Python 3.10 or higher (Python 3.15 is supported out of the box).
- Any modern web browser (Chrome, Firefox, Safari, Edge).

### Running the Application

```bash
# 1. Navigate to project directory
cd /Users/manojkakumanu/Downloads/ai

# 2. Launch server
python3 run.py 8000
```

Open your browser to:
```
http://127.0.0.1:8000
```

---

## 5. Running Automated Unit Tests

To run the complete automated test suite verifying database transactions, recommendation logic, and upload parsing:

```bash
python3 -m unittest discover -s tests -v
```

---

## 6. Security & Privacy Notes

- All study notes, quiz scores, and learning progress remain strictly on your local machine in SQLite (`data/learning_os.db`).
- No personal study materials or notes are transmitted to third-party AI services without user configuration.
- To configure external cloud providers, copy `.env.example` to `.env` and populate your API credentials.

