"""
AI Engineer Learning OS - Document & Notes Upload Analyzer
Extracts text from documents, code files, and study notes. Matches concepts
against the 12-stage AI Engineering roadmap and categorizes findings into
the required 3 Groups: (A) Found, (B) Already Learned, and (C) Missing/Further Study.
"""

import re
import os
import json
from typing import Dict, Any, List, Tuple
from backend.roadmap_data import TOPICS, STAGES, get_topic_by_id


# Keyword and concept signature dictionary mapping topic IDs to regex patterns and terms
TOPIC_SIGNATURES: Dict[str, Dict[str, Any]] = {
    "py_syntax": {
        "keywords": ["variable", "syntax", "print", "data type", "type hint", "int", "float", "string", "bool", "assignment"],
        "formulas": [],
        "weight": 1.0
    },
    "py_loops": {
        "keywords": ["for loop", "while loop", "loop", "loops", "conditions", "if-elif", "enumerate", "zip", "iteration", "list comprehension", "break", "continue"],
        "formulas": [],
        "weight": 1.0
    },
    "py_functions": {
        "keywords": ["def", "function", "functions", "return", "args", "kwargs", "scope", "lambda", "docstring", "parameter"],
        "formulas": [],
        "weight": 1.0
    },
    "py_data_structures": {
        "keywords": ["list", "tuple", "dictionary", "dict", "set", "hash map", "key-value", "pop", "append"],
        "formulas": [],
        "weight": 1.0
    },
    "py_oop": {
        "keywords": ["class", "object", "inheritance", "dunder", "__init__", "self", "polymorphism", "dataclass", "method"],
        "formulas": [],
        "weight": 1.1
    },
    "math_vectors_matrices": {
        "keywords": ["vector", "matrix", "matrices", "dimension", "transpose", "linear algebra", "magnitude", "coordinate"],
        "formulas": ["A^T", "R^n", "[x, y, z]"],
        "weight": 1.2
    },
    "math_dot_products": {
        "keywords": ["dot product", "cosine similarity", "scalar product", "orthogonal", "projection", "inner product"],
        "formulas": ["u . v", "cos(theta)", "|u||v|"],
        "weight": 1.3
    },
    "math_derivatives_gradients": {
        "keywords": ["derivative", "gradient", "slope", "rate of change", "tangent", "partial derivative", "nabla"],
        "formulas": ["df/dx", "dy/dx", "nabla f", "partial"],
        "weight": 1.3
    },
    "math_chain_rule": {
        "keywords": ["chain rule", "composite function", "backprop", "computational graph", "error gradient"],
        "formulas": ["dz/dx = dz/dy * dy/dx"],
        "weight": 1.4
    },
    "data_numpy": {
        "keywords": ["numpy", "np.array", "ndarray", "broadcasting", "vectorized", "axis", "reshape", "np.dot", "matmul"],
        "formulas": [],
        "weight": 1.2
    },
    "data_pandas": {
        "keywords": ["pandas", "dataframe", "series", "read_csv", "loc", "iloc", "groupby", "merge", "value_counts"],
        "formulas": [],
        "weight": 1.2
    },
    "data_cleaning": {
        "keywords": ["missing values", "dropna", "fillna", "imputation", "outlier", "iqr", "duplicates", "z-score", "null"],
        "formulas": ["Q3 - Q1", "(x - mu) / sigma"],
        "weight": 1.2
    },
    "ml_foundations": {
        "keywords": ["supervised learning", "unsupervised learning", "reinforcement learning", "features", "labels", "target"],
        "formulas": ["y = f(X)"],
        "weight": 1.1
    },
    "ml_linear_regression": {
        "keywords": ["linear regression", "weights", "bias", "mean squared error", "mse", "residuals", "r-squared", "slope intercept"],
        "formulas": ["y = wx + b", "MSE = 1/n sum((y - y_hat)^2)"],
        "weight": 1.3
    },
    "ml_gradient_descent": {
        "keywords": ["gradient descent", "learning rate", "sgd", "batch gradient", "loss surface", "step size", "convergence"],
        "formulas": ["w = w - eta * grad", "w := w - alpha * dJ/dw"],
        "weight": 1.3
    },
    "ml_logistic_regression": {
        "keywords": ["logistic regression", "sigmoid", "binary classification", "log-odds", "cross-entropy", "decision boundary"],
        "formulas": ["1 / (1 + e^-z)", "log(p / (1-p))"],
        "weight": 1.3
    },
    "ml_eval_metrics": {
        "keywords": ["confusion matrix", "precision", "recall", "f1-score", "true positive", "false positive", "roc-auc", "accuracy"],
        "formulas": ["TP / (TP + FP)", "2 * (P * R) / (P + R)"],
        "weight": 1.3
    },
    "ml_trees_forests": {
        "keywords": ["decision tree", "random forest", "gini impurity", "entropy", "information gain", "bagging", "ensemble"],
        "formulas": ["1 - sum(p_i^2)"],
        "weight": 1.3
    },
    "ml_gradient_boosting": {
        "keywords": ["xgboost", "lightgbm", "catboost", "gradient boosting", "residual", "shrinkage", "boosting"],
        "formulas": [],
        "weight": 1.4
    },
    "dl_neurons": {
        "keywords": ["perceptron", "artificial neuron", "activation function", "relu", "sigmoid", "tanh", "gelu", "bias"],
        "formulas": ["z = sum(w_i * x_i) + b", "max(0, x)"],
        "weight": 1.3
    },
    "dl_backprop": {
        "keywords": ["backpropagation", "loss function", "backward pass", "autograd", "vanishing gradient", "computational graph"],
        "formulas": ["dL/dw = dL/dy * dy/dz * dz/dw"],
        "weight": 1.5
    },
    "dl_pytorch_tensors": {
        "keywords": ["pytorch", "torch.tensor", "cuda", "requires_grad", "device", "backward()", "torch.nn"],
        "formulas": [],
        "weight": 1.3
    },
    "snn_cnn": {
        "keywords": ["convolution", "cnn", "filter", "kernel", "stride", "padding", "max pooling", "feature map"],
        "formulas": ["(W - F + 2P)/S + 1"],
        "weight": 1.4
    },
    "snn_transformers": {
        "keywords": ["transformer", "self-attention", "multi-head attention", "positional encoding", "encoder", "decoder"],
        "formulas": ["Attention(Q, K, V) = softmax(QK^T / sqrt(d_k))V"],
        "weight": 1.5
    },
    "snn_qkv": {
        "keywords": ["query", "key", "value", "qkv", "scaled dot-product", "attention weight", "d_k"],
        "formulas": ["QK^T / sqrt(d_k)"],
        "weight": 1.5
    },
    "llm_tokenization": {
        "keywords": ["tokenizer", "tokenization", "byte-pair encoding", "bpe", "vocab", "token id", "subword", "tiktoken"],
        "formulas": [],
        "weight": 1.3
    },
    "llm_prompt_engineering": {
        "keywords": ["prompt engineering", "few-shot", "zero-shot", "chain of thought", "system prompt", "temperature", "top-p"],
        "formulas": [],
        "weight": 1.2
    },
    "llm_structured_outputs": {
        "keywords": ["structured output", "json mode", "pydantic", "schema validation", "function call", "constrained generation"],
        "formulas": [],
        "weight": 1.3
    },
    "rag_foundations": {
        "keywords": ["rag", "retrieval augmented generation", "vector search", "chunking", "knowledge base", "groundedness"],
        "formulas": [],
        "weight": 1.4
    },
    "rag_vector_db": {
        "keywords": ["vector database", "pinecone", "chroma", "hnsw", "approximate nearest neighbor", "pgvector", "qdrant"],
        "formulas": [],
        "weight": 1.4
    },
    "agent_tools_calling": {
        "keywords": ["agent", "tool calling", "function calling", "react loop", "autonomous", "tool use", "planning"],
        "formulas": [],
        "weight": 1.4
    },
    "be_fastapi": {
        "keywords": ["fastapi", "uvicorn", "endpoint", "rest api", "pydantic", "async def", "request", "response"],
        "formulas": [],
        "weight": 1.3
    },
    "adv_lora_peft": {
        "keywords": ["lora", "qlora", "peft", "low-rank adaptation", "fine-tuning", "adapter", "rank r", "alpha"],
        "formulas": ["W = W_0 + B * A"],
        "weight": 1.6
    }
}


def extract_text_from_content(content_bytes: bytes, filename: str) -> Tuple[str, str, Dict[str, Any]]:
    """
    Extract readable text from uploaded file.
    Supports text, markdown, python, json, and handles image/pdf parsing transparently.
    Returns (extracted_text, parser_type, diagnostic_metadata).
    """
    ext = os.path.splitext(filename)[1].lower()
    text = ""
    parser_type = "plain_text"
    diagnostics = {"filename": filename, "size_bytes": len(content_bytes)}

    if ext in [".txt", ".md", ".py", ".json", ".csv", ".html", ".log"]:
        try:
            text = content_bytes.decode("utf-8")
            parser_type = f"text_{ext[1:]}"
        except UnicodeDecodeError:
            try:
                text = content_bytes.decode("latin-1")
                parser_type = f"text_{ext[1:]}_fallback"
            except Exception as e:
                text = ""
                diagnostics["error"] = f"Decoding failed: {str(e)}"

    elif ext in [".png", ".jpg", ".jpeg", ".webp"]:
        # Honest fallback note: No external OCR API key or tesseract binary configured by default.
        # We extract any clean embedded ASCII strings / metadata and inform the user honestly.
        parser_type = "image_ascii_scan"
        ascii_matches = re.findall(b"[a-zA-Z0-9_, =.(){}\\[\\]\\+\\-*\\/\\n]{4,}", content_bytes)
        decoded_snippets = []
        for m in ascii_matches:
            try:
                s = m.decode("ascii", errors="ignore").strip()
                if len(s) > 5:
                    decoded_snippets.append(s)
            except Exception:
                pass
        text = "\n".join(decoded_snippets)
        diagnostics["ocr_status"] = "Local heuristic scanner active (Cloud OCR API key not configured)."
        diagnostics["note"] = "Extracting legible text patterns and keyword signatures directly."

    elif ext == ".pdf":
        parser_type = "pdf_text_extractor"
        # Extract text stream segments
        text_segments = re.findall(rb"\((.*?)\) *T[jJ]", content_bytes)
        if text_segments:
            lines = [seg.decode("latin-1", errors="ignore") for seg in text_segments]
            text = " ".join(lines)
        else:
            # Fallback to plain ascii regex extraction
            ascii_matches = re.findall(b"[a-zA-Z0-9_, =.(){}\\[\\]\\+\\-*\\/\\n]{4,}", content_bytes)
            text = "\n".join([m.decode("ascii", errors="ignore").strip() for m in ascii_matches if len(m) > 5])
        diagnostics["pdf_status"] = "Native stream extraction performed."

    else:
        # Generic fallback
        parser_type = "generic_binary_scan"
        text = content_bytes.decode("utf-8", errors="ignore")
        diagnostics["status"] = "Generic text decoding applied."

    return text, parser_type, diagnostics


def match_concepts_to_roadmap(
    text: str,
    progress_map: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Analyzes extracted text and matches against roadmap topics.
    Returns the three mandatory groups:
    Group A: Topics found in the material (with match snippets and confidence).
    Group B: Topics already recorded as learned/mastered by the user.
    Group C: Topics missing or requiring further prerequisite study.
    """
    text_lower = text.lower()
    found_topics = []

    for topic in TOPICS:
        tid = topic["id"]
        sig = TOPIC_SIGNATURES.get(tid)
        
        # Check topic title and key concepts
        title_matches = topic["title"].lower() in text_lower
        matched_keywords = []
        matched_formulas = []
        
        # Check custom signatures
        if sig:
            for kw in sig["keywords"]:
                if kw.lower() in text_lower:
                    matched_keywords.append(kw)
            for f in sig.get("formulas", []):
                if f.lower() in text_lower:
                    matched_formulas.append(f)

        # Check topic key_concepts
        for kc in topic.get("key_concepts", []):
            if kc.lower() in text_lower and kc.lower() not in [k.lower() for k in matched_keywords]:
                matched_keywords.append(kc)

        # Score matching confidence
        score = 0
        if title_matches:
            score += 40
        score += min(len(matched_keywords) * 15, 60)
        score += min(len(matched_formulas) * 20, 40)

        # Snippet extraction (find first matching sentence)
        snippet = ""
        sample_term = matched_keywords[0] if matched_keywords else (topic["title"].split()[0] if title_matches else None)
        if sample_term:
            idx = text_lower.find(sample_term.lower())
            if idx != -1:
                start = max(0, idx - 40)
                end = min(len(text), idx + 100)
                snippet = "..." + text[start:end].replace("\n", " ").strip() + "..."

        if score >= 30:
            found_topics.append({
                "topic_id": tid,
                "title": topic["title"],
                "stage_id": topic["stage_id"],
                "stage_name": STAGES[topic["stage_id"] - 1]["name"],
                "match_score": min(score, 100),
                "matched_terms": matched_keywords[:5],
                "matched_formulas": matched_formulas,
                "context_snippet": snippet,
                "prerequisites": topic.get("prerequisites", [])
            })

    # Sort found topics by match score descending
    found_topics.sort(key=lambda x: x["match_score"], reverse=True)

    # Group A: Topics found in the uploaded material
    group_a = found_topics

    # Group B: Found topics that are ALREADY recorded as learned/mastered by the user
    group_b = []
    for item in found_topics:
        tid = item["topic_id"]
        user_p = progress_map.get(tid, {})
        if user_p.get("status") in ("mastered", "in_progress"):
            group_b.append({
                "topic_id": tid,
                "title": item["title"],
                "stage_id": item["stage_id"],
                "status": user_p.get("status"),
                "confidence_rating": user_p.get("confidence_rating", 1),
                "last_studied_date": user_p.get("last_studied_date")
            })

    # Group C: Missing prerequisites or foundational gaps for the topics found
    group_c_map = {}
    for item in found_topics:
        for prereq_id in item.get("prerequisites", []):
            pt = get_topic_by_id(prereq_id)
            if pt:
                prereq_prog = progress_map.get(prereq_id, {})
                status = prereq_prog.get("status", "not_started")
                if status != "mastered":
                    if prereq_id not in group_c_map:
                        group_c_map[prereq_id] = {
                            "topic_id": prereq_id,
                            "title": pt["title"],
                            "stage_id": pt["stage_id"],
                            "stage_name": STAGES[pt["stage_id"] - 1]["name"],
                            "status": status,
                            "required_by": [item["title"]],
                            "reason": f"Prerequisite for '{item['title']}', but your status is '{status}'."
                        }
                    else:
                        group_c_map[prereq_id]["required_by"].append(item["title"])

    group_c = list(group_c_map.values())

    return {
        "group_a_found": group_a,
        "group_b_already_learned": group_b,
        "group_c_missing_or_further_study": group_c,
        "total_concepts_detected": len(found_topics),
        "text_length": len(text)
    }
