"""
AI Engineer Learning OS - Complete 12-Stage Roadmap Data
Covers all 12 stages from Programming Foundations to Advanced AI Engineering.
Each topic includes prerequisites, stage metadata, difficulty, estimated hours,
and practical real-world AI applications.
"""

from typing import List, Dict, Any

STAGES = [
    {
        "id": 1,
        "name": "Programming Foundations",
        "slug": "programming-foundations",
        "description": "Master Python fundamentals, software engineering discipline, data structures, and terminal tools essential for every AI engineer.",
        "badge": "Core Foundation",
        "icon": "code",
        "practical_projects": [
            {
                "id": "proj_1_calc",
                "title": "Configurable Scientific Calculator & Vector Math Tool",
                "difficulty": "Beginner",
                "description": "Build a command-line scientific tool that performs linear equations, basic statistics, and vector dot products from scratch.",
                "prerequisites": ["py_syntax", "py_functions", "py_errors"]
            },
            {
                "id": "proj_1_organizer",
                "title": "Automated Dataset File Organizer",
                "difficulty": "Beginner",
                "description": "Script that scans directories of images and text, organizes them into train/val folders, renames systematically, and logs metadata.",
                "prerequisites": ["py_files", "py_modules", "py_terminal"]
            },
            {
                "id": "proj_1_csv_analyzer",
                "title": "Pure Python CSV Data Analyzer",
                "difficulty": "Beginner",
                "description": "Parse, clean, and summarize large CSV datasets without external libraries using pure Python data structures.",
                "prerequisites": ["py_data_structures", "py_oop", "py_files"]
            },
            {
                "id": "proj_1_api_collector",
                "title": "ArXiv Research Paper Collector",
                "difficulty": "Beginner+",
                "description": "Collect AI research paper abstracts from the ArXiv API, parse XML/JSON responses, handle rate limits, and save to structured JSONL.",
                "prerequisites": ["py_errors", "py_modules", "py_virtual_envs"]
            }
        ]
    },
    {
        "id": 2,
        "name": "Mathematics for AI",
        "slug": "mathematics-for-ai",
        "description": "Build visual and geometric intuition for linear algebra, calculus, probability, and optimization before diving into models.",
        "badge": "Core Foundation",
        "icon": "sigma",
        "practical_projects": [
            {
                "id": "proj_2_matrix_engine",
                "title": "Matrix & Vector Math Engine from Scratch",
                "difficulty": "Intermediate",
                "description": "Implement matrix multiplication, vector projections, dot product cosine similarity, and transpose without external math libraries.",
                "prerequisites": ["math_vectors_matrices", "math_dot_products"]
            },
            {
                "id": "proj_2_gradient_visualizer",
                "title": "Interactive 2D/3D Gradient Descent Simulator",
                "difficulty": "Intermediate",
                "description": "Simulate gradient descent finding the minimum of loss surfaces (convex vs non-convex), demonstrating learning rate divergence.",
                "prerequisites": ["math_derivatives_gradients", "math_optimization"]
            }
        ]
    },
    {
        "id": 3,
        "name": "Data Analysis and Processing",
        "slug": "data-analysis-processing",
        "description": "Wrangle, clean, scale, and visualize tabular and unstructured data using NumPy, Pandas, Matplotlib, and SQL.",
        "badge": "Practical Data",
        "icon": "database",
        "practical_projects": [
            {
                "id": "proj_3_sales_eda",
                "title": "Exploratory Data Analysis Dashboard",
                "difficulty": "Intermediate",
                "description": "Perform comprehensive statistical EDA on a real-world dataset: detect outliers, impute missing values, and uncover feature correlations.",
                "prerequisites": ["data_numpy", "data_pandas", "data_matplotlib", "data_eda"]
            },
            {
                "id": "proj_3_clean_pipeline",
                "title": "Production-Grade Feature Engineering Pipeline",
                "difficulty": "Intermediate",
                "description": "Build a leak-free preprocessing pipeline that handles categorical encoding, standard scaling, and train/val/test splits safely.",
                "prerequisites": ["data_cleaning", "data_encoding", "data_scaling", "data_leakage"]
            }
        ]
    },
    {
        "id": 4,
        "name": "Machine Learning",
        "slug": "machine-learning",
        "description": "Master classic supervised and unsupervised algorithms, loss functions, regularization, and model evaluation metrics.",
        "badge": "Applied ML",
        "icon": "cpu",
        "practical_projects": [
            {
                "id": "proj_4_house_pricing",
                "title": "End-to-End Real Estate Price Predictor",
                "difficulty": "Intermediate",
                "description": "Train, tune, and evaluate regularized linear models (Ridge/Lasso) and Gradient Boosted trees with cross-validation and feature importance.",
                "prerequisites": ["ml_linear_regression", "ml_gradient_descent", "ml_regularization", "ml_eval_metrics"]
            },
            {
                "id": "proj_4_spam_classifier",
                "title": "Production SMS & Email Spam Classifier",
                "difficulty": "Intermediate",
                "description": "Build an end-to-end text classification pipeline using TF-IDF and Naive Bayes/Logistic Regression with high precision thresholding.",
                "prerequisites": ["ml_logistic_regression", "ml_naive_bayes", "ml_sklearn_pipelines"]
            },
            {
                "id": "proj_4_customer_segmentation",
                "title": "Customer Segmentation with K-Means & PCA",
                "difficulty": "Intermediate",
                "description": "Cluster multidimensional customer spending habits using PCA for 2D visualization and silhouette analysis for optimal K.",
                "prerequisites": ["ml_kmeans", "ml_pca"]
            }
        ]
    },
    {
        "id": 5,
        "name": "Deep Learning",
        "slug": "deep-learning",
        "description": "Understand artificial neurons, forward/backward propagation, activation functions, optimizers, and PyTorch fundamentals.",
        "badge": "Deep Learning",
        "icon": "network",
        "practical_projects": [
            {
                "id": "proj_5_nn_from_scratch",
                "title": "Multilayer Perceptron from Scratch with NumPy",
                "difficulty": "Advanced",
                "description": "Derive and code forward propagation, cross-entropy loss, backpropagation calculus, and SGD parameter updates purely in NumPy.",
                "prerequisites": ["dl_neurons", "dl_forward_prop", "dl_backprop", "dl_optimizers"]
            },
            {
                "id": "proj_5_pytorch_mnist",
                "title": "PyTorch Handwritten Digit Classifier & Checkpointer",
                "difficulty": "Intermediate",
                "description": "Build a PyTorch Dataset, DataLoader, model architecture, training loop with learning rate scheduling, and checkpoint saving.",
                "prerequisites": ["dl_pytorch_tensors", "dl_training_loop", "dl_regularization"]
            }
        ]
    },
    {
        "id": 6,
        "name": "Specialized Neural Networks",
        "slug": "specialized-neural-networks",
        "description": "Dive into CNNs for computer vision, RNNs/LSTMs for sequences, and the modern Transformer architecture with Self-Attention.",
        "badge": "Architectures",
        "icon": "layers",
        "practical_projects": [
            {
                "id": "proj_6_vision_transfer",
                "title": "Transfer Learning Vision Classifier",
                "difficulty": "Advanced",
                "description": "Fine-tune a pretrained ResNet/Vision Transformer on custom image data with data augmentation and freeze/unfreeze stages.",
                "prerequisites": ["snn_cnn", "snn_transfer_learning"]
            },
            {
                "id": "proj_6_attention_viz",
                "title": "Interactive Multi-Head Attention Visualizer",
                "difficulty": "Advanced",
                "description": "Calculate Query, Key, Value dot-product attention scores in PyTorch and render heatmaps revealing token relationships.",
                "prerequisites": ["snn_attention", "snn_transformers", "snn_qkv"]
            }
        ]
    },
    {
        "id": 7,
        "name": "Natural Language Processing and LLMs",
        "slug": "nlp-and-llms",
        "description": "Harness Large Language Models: tokenization, prompt engineering, context windows, structured outputs, streaming, and API integration.",
        "badge": "Modern LLMs",
        "icon": "message-square",
        "practical_projects": [
            {
                "id": "proj_7_doc_summarizer",
                "title": "Multi-Strategy Document Summarization Tool",
                "difficulty": "Intermediate",
                "description": "Build Map-Reduce and Refine summarization flows for documents exceeding LLM context windows with streaming responses.",
                "prerequisites": ["llm_context_windows", "llm_prompt_engineering", "llm_api_integration"]
            },
            {
                "id": "proj_7_structured_extractor",
                "title": "Pydantic-Enforced Structured Extraction Pipeline",
                "difficulty": "Intermediate",
                "description": "Extract complex entities (invoices, resumes, contracts) with strict JSON schema validation, retry loops, and hallucination checks.",
                "prerequisites": ["llm_structured_outputs", "llm_hallucinations"]
            }
        ]
    },
    {
        "id": 8,
        "name": "Retrieval-Augmented Generation (RAG)",
        "slug": "retrieval-augmented-generation",
        "description": "Connect LLMs to custom knowledge bases using chunking, vector embeddings, vector databases, hybrid search, reranking, and source attribution.",
        "badge": "Production RAG",
        "icon": "search",
        "practical_projects": [
            {
                "id": "proj_8_chat_with_pdf",
                "title": "Grounded Chat with PDF Engine",
                "difficulty": "Advanced",
                "description": "Build an end-to-end PDF question-answering app with recursive chunking, cosine vector similarity, and clickable source page citations.",
                "prerequisites": ["rag_chunking", "rag_embeddings", "rag_vector_db", "rag_grounded_gen"]
            },
            {
                "id": "proj_8_hybrid_rerank",
                "title": "Production Hybrid Search & Cross-Encoder Reranker",
                "difficulty": "Advanced",
                "description": "Combine BM25 keyword search with dense vector retrieval using Reciprocal Rank Fusion and a cross-encoder reranking step.",
                "prerequisites": ["rag_hybrid_search", "rag_reranking", "rag_evaluation"]
            }
        ]
    },
    {
        "id": 9,
        "name": "AI Agents and Tool Use",
        "slug": "ai-agents-and-tool-use",
        "description": "Transition from chatbots to autonomous reasoning systems: function calling, tool selection, persistent memory, planning, and guardrails.",
        "badge": "AI Agents",
        "icon": "bot",
        "practical_projects": [
            {
                "id": "proj_9_research_agent",
                "title": "Autonomous Multi-Step Research Agent",
                "difficulty": "Advanced",
                "description": "Build a ReAct (Reason + Act) loop agent equipped with web search, calculator, and file writing tools with cycle prevention.",
                "prerequisites": ["agent_tools_calling", "agent_state_memory", "agent_planning"]
            },
            {
                "id": "proj_9_human_in_loop",
                "title": "Human-in-the-Loop Safe Action Orchestrator",
                "difficulty": "Advanced",
                "description": "Agent workflow that decomposes complex multi-step execution plans and pauses for human verification before destructive steps.",
                "prerequisites": ["agent_human_approval", "agent_guardrails"]
            }
        ]
    },
    {
        "id": 10,
        "name": "Backend and AI Application Development",
        "slug": "backend-and-ai-app-dev",
        "description": "Build robust, scalable APIs to serve AI models: FastAPI, async I/O, validation, rate limiting, Docker, and caching.",
        "badge": "Engineering Systems",
        "icon": "server",
        "practical_projects": [
            {
                "id": "proj_10_ai_api",
                "title": "Production FastAPI AI Gateway",
                "difficulty": "Advanced",
                "description": "FastAPI service with JWT auth, token bucket rate limiting, Redis response caching, streaming SSE endpoints, and Dockerfile.",
                "prerequisites": ["be_fastapi", "be_pydantic", "be_async", "be_docker"]
            }
        ]
    },
    {
        "id": 11,
        "name": "AI Deployment and MLOps",
        "slug": "ai-deployment-and-mlops",
        "description": "Deploy, monitor, and maintain models in production: containerization, CI/CD, data drift detection, latency optimization, and quantization.",
        "badge": "MLOps",
        "icon": "activity",
        "practical_projects": [
            {
                "id": "proj_11_drift_monitor",
                "title": "Live Model Drift & Performance Monitor",
                "difficulty": "Advanced",
                "description": "Statistical drift detection service that alerts when incoming production inference distributions deviate significantly from training baseline.",
                "prerequisites": ["ops_model_serving", "ops_drift_detection", "ops_monitoring"]
            }
        ]
    },
    {
        "id": 12,
        "name": "Advanced AI Engineering",
        "slug": "advanced-ai-engineering",
        "description": "Fine-tuning with LoRA/QLoRA, GPU memory optimization, LLM evaluations, red teaming, prompt injection defense, and AI system design.",
        "badge": "Advanced Mastery",
        "icon": "shield-check",
        "practical_projects": [
            {
                "id": "proj_12_peft_lora",
                "title": "LoRA Fine-Tuning of Small Open-Weight Model",
                "difficulty": "Master",
                "description": "Parameter-efficient fine-tuning (PEFT/LoRA) on custom domain task, evaluating before/after perplexity and task accuracy.",
                "prerequisites": ["adv_lora_peft", "adv_gpu_memory", "adv_eval_frameworks"]
            },
            {
                "id": "proj_12_security_guard",
                "title": "Enterprise LLM Guardrail & Prompt Defense System",
                "difficulty": "Master",
                "description": "Defense-in-depth security filter detecting prompt injections, jailbreaks, PII leakage, and toxic hallucinations.",
                "prerequisites": ["adv_security_prompt_injection", "adv_responsible_ai"]
            }
        ]
    }
]

# Comprehensive Roadmap Topics
TOPICS: List[Dict[str, Any]] = [
    # ================= STAGE 1: Programming Foundations =================
    {
        "id": "py_syntax",
        "stage_id": 1,
        "title": "Python Syntax and Variables",
        "difficulty": "Beginner",
        "estimated_hours": 3,
        "prerequisites": [],
        "importance": "The fundamental building block of all AI engineering code. Python is the lingua franca of machine learning.",
        "what_you_will_do": "Write clean, idiomatic Python scripts, declare variables with explicit types, and execute your first AI scripts.",
        "key_concepts": ["Variables", "Primitive types (int, float, str, bool)", "Naming conventions", "Type hints", "Print formatting"]
    },
    {
        "id": "py_operators",
        "stage_id": 1,
        "title": "Data Types and Operators",
        "difficulty": "Beginner",
        "estimated_hours": 2,
        "prerequisites": ["py_syntax"],
        "importance": "Underpins mathematical computations and logic checks inside neural networks and data manipulation algorithms.",
        "what_you_will_do": "Perform arithmetic, logical comparisons, boolean masks, and bitwise operations.",
        "key_concepts": ["Arithmetic operators", "Comparison operators", "Logical operators", "Type casting"]
    },
    {
        "id": "py_loops",
        "stage_id": 1,
        "title": "Conditions and Loops",
        "difficulty": "Beginner",
        "estimated_hours": 3,
        "prerequisites": ["py_operators"],
        "importance": "Iterating over datasets, training epochs, batches, and token streams requires mastery of control flow.",
        "what_you_will_do": "Write robust if-elif-else branches, for-loops, while-loops, list comprehensions, and break/continue statements.",
        "key_concepts": ["if-elif-else", "for loop", "while loop", "enumerate", "zip", "list comprehensions"]
    },
    {
        "id": "py_functions",
        "stage_id": 1,
        "title": "Functions and Scope",
        "difficulty": "Beginner",
        "estimated_hours": 4,
        "prerequisites": ["py_loops"],
        "importance": "Reusable modular code is essential for training pipelines, preprocessing transforms, and model architectures.",
        "what_you_will_do": "Design modular functions with *args, **kwargs, default parameters, docstrings, type signatures, and pure side-effect-free logic.",
        "key_concepts": ["def", "Return values", "Parameters and arguments", "Scope (LEGB)", "Lambda functions", "Docstrings"]
    },
    {
        "id": "py_data_structures",
        "stage_id": 1,
        "title": "Lists, Tuples, Sets, and Dictionaries",
        "difficulty": "Beginner",
        "estimated_hours": 4,
        "prerequisites": ["py_functions"],
        "importance": "Representing embeddings, token maps, vocabularies, and batch tensors depends on knowing the right data structure.",
        "what_you_will_do": "Select optimal collection types, use hash maps for O(1) lookups in tokenizers, and manipulate nested JSON payloads.",
        "key_concepts": ["Lists vs Tuples", "Dictionaries & hash maps", "Sets & set operations", "Time complexity intuition"]
    },
    {
        "id": "py_strings",
        "stage_id": 1,
        "title": "String Manipulation and Regex",
        "difficulty": "Beginner",
        "estimated_hours": 3,
        "prerequisites": ["py_data_structures"],
        "importance": "Text cleaning and prompt parsing constitute 60% of modern LLM and NLP engineering.",
        "what_you_will_do": "Clean messy web crawls, parse markdown, extract URLs/entities with regular expressions, and format prompt templates.",
        "key_concepts": ["f-strings", "split/join", "Regex patterns", "Encoding (UTF-8)", "Sanitization"]
    },
    {
        "id": "py_errors",
        "stage_id": 1,
        "title": "Error Handling and Debugging",
        "difficulty": "Beginner+",
        "estimated_hours": 3,
        "prerequisites": ["py_functions"],
        "importance": "Production AI pipelines encounter corrupted image files, malformed JSON, and API timeouts.",
        "what_you_will_do": "Write defensive code using try-except-finally blocks, raise custom exceptions, and step through code with Python debugger (pdb).",
        "key_concepts": ["try-except-finally", "Custom exceptions", "pdb debugging", "Logging vs printing"]
    },
    {
        "id": "py_files",
        "stage_id": 1,
        "title": "File Handling (JSON, CSV, Binary)",
        "difficulty": "Beginner+",
        "estimated_hours": 3,
        "prerequisites": ["py_errors"],
        "importance": "AI models ingest gigabytes of data from disk and save model weights, checkpoints, and logs.",
        "what_you_will_do": "Read and write text, JSON, CSV, and binary pickle/safetensors files safely with context managers.",
        "key_concepts": ["with statement context managers", "json module", "csv module", "Pathlib", "Streaming large files"]
    },
    {
        "id": "py_modules",
        "stage_id": 1,
        "title": "Modules and Packages",
        "difficulty": "Beginner+",
        "estimated_hours": 2,
        "prerequisites": ["py_files"],
        "importance": "Organizing production codebases across files and directories cleanly.",
        "what_you_will_do": "Structure reusable Python packages with `__init__.py`, import relative and absolute modules, and avoid circular imports.",
        "key_concepts": ["import mechanics", "__init__.py", "__name__ == '__main__'", "Package directory structures"]
    },
    {
        "id": "py_oop",
        "stage_id": 1,
        "title": "Object-Oriented Programming (OOP)",
        "difficulty": "Intermediate",
        "estimated_hours": 5,
        "prerequisites": ["py_modules"],
        "importance": "PyTorch models, custom transformers, Scikit-learn estimators, and agent tools are all built as OOP classes.",
        "what_you_will_do": "Create classes, instantiate objects, inherit from PyTorch's `nn.Module`, override dunder methods (`__call__`, `__len__`, `__getitem__`).",
        "key_concepts": ["Classes & Objects", "self & __init__", "Inheritance & Polymorphism", "Dunder methods", "Dataclasses"]
    },
    {
        "id": "py_virtual_envs",
        "stage_id": 1,
        "title": "Virtual Environments & Package Management",
        "difficulty": "Beginner+",
        "estimated_hours": 2,
        "prerequisites": ["py_modules"],
        "importance": "Eliminates 'it works on my machine' dependency conflicts across PyTorch, CUDA, and library versions.",
        "what_you_will_do": "Create and isolate environments with venv/conda/uv, pin exact reproducible versions with requirements.txt or pyproject.toml.",
        "key_concepts": ["venv / conda", "pip freeze", "pyproject.toml", "Dependency locks", "CUDA version pairing"]
    },
    {
        "id": "py_git",
        "stage_id": 1,
        "title": "Git and GitHub for AI Projects",
        "difficulty": "Beginner+",
        "estimated_hours": 3,
        "prerequisites": ["py_syntax"],
        "importance": "Industry standard for version controlling code, collaborating with teams, and publishing open-source models.",
        "what_you_will_do": "Initialize repos, commit changes, branch, resolve merge conflicts, and write `.gitignore` to never leak API keys or large model weights.",
        "key_concepts": ["git init/clone/commit", "Branching & PRs", ".gitignore for weights & keys", "Git LFS"]
    },
    {
        "id": "py_terminal",
        "stage_id": 1,
        "title": "Basic Terminal & Shell Usage",
        "difficulty": "Beginner",
        "estimated_hours": 2,
        "prerequisites": [],
        "importance": "Training jobs, cloud GPUs, and Docker containers are controlled exclusively via the command line.",
        "what_you_will_do": "Navigate file trees, inspect processes, run background jobs, monitor memory, and manipulate pipes and redirects.",
        "key_concepts": ["cd, ls, mkdir, rm", "cat, grep, head, tail", "Piping and redirection", "Environment variables", "htop/ps"]
    },

    # ================= STAGE 2: Mathematics for AI =================
    {
        "id": "math_vectors_matrices",
        "stage_id": 2,
        "title": "Vectors and Matrices (Geometric Intuition)",
        "difficulty": "Beginner+",
        "estimated_hours": 4,
        "prerequisites": ["py_syntax"],
        "importance": "Data points, embeddings, image pixels, and neural weights are all vectors and matrices in high-dimensional space.",
        "what_you_will_do": "Visualize vectors as arrows and coordinate points, compute matrix dimensions, and perform transpose operations.",
        "key_concepts": ["Vector magnitude & direction", "Matrix rows x cols", "Transpose", "Geometric coordinate transforms"]
    },
    {
        "id": "math_dot_products",
        "stage_id": 2,
        "title": "Dot Products and Vector Similarity",
        "difficulty": "Intermediate",
        "estimated_hours": 3,
        "prerequisites": ["math_vectors_matrices"],
        "importance": "Dot product is the fundamental computation in Transformer self-attention, RAG similarity search, and linear regression.",
        "what_you_will_do": "Calculate dot products geometrically and algebraically, and compute cosine similarity between text embeddings.",
        "key_concepts": ["Dot product formula", "Orthogonality (perpendicular vectors)", "Cosine similarity", "Projection"]
    },
    {
        "id": "math_derivatives_gradients",
        "stage_id": 2,
        "title": "Derivatives and Gradients (Slope Intuition)",
        "difficulty": "Intermediate",
        "estimated_hours": 4,
        "prerequisites": ["math_vectors_matrices"],
        "importance": "Gradients tell the neural network which direction to nudge each weight to decrease error.",
        "what_you_will_do": "Interpret derivatives as rates of change, visualize gradient vectors pointing to steepest ascent, and calculate basic slopes.",
        "key_concepts": ["Instantaneous rate of change", "Tangent line", "Partial derivatives", "Gradient vector"]
    },
    {
        "id": "math_chain_rule",
        "stage_id": 2,
        "title": "The Chain Rule & Backpropagation Math",
        "difficulty": "Intermediate+",
        "estimated_hours": 4,
        "prerequisites": ["math_derivatives_gradients"],
        "importance": "The mathematical engine powering the entire deep learning revolution.",
        "what_you_will_do": "Apply the chain rule to composite functions f(g(x)) and compute error propagation through multi-layer computational graphs.",
        "key_concepts": ["Composite function derivatives", "Computational graphs", "Forward pass vs backward pass"]
    },
    {
        "id": "math_probability",
        "stage_id": 2,
        "title": "Probability, Bayes' Theorem, and Distributions",
        "difficulty": "Intermediate",
        "estimated_hours": 4,
        "prerequisites": ["math_vectors_matrices"],
        "importance": "AI outputs are probabilistic distributions (e.g. next-token logits, classification softmax confidence).",
        "what_you_will_do": "Calculate conditional probabilities, apply Bayes' Rule, and understand Normal/Gaussian, Uniform, and Categorical distributions.",
        "key_concepts": ["Independent vs dependent events", "P(A|B) Bayes' Theorem", "Normal/Gaussian curve", "Softmax probabilities"]
    },
    {
        "id": "math_optimization",
        "stage_id": 2,
        "title": "Optimization Intuition & Loss Surfaces",
        "difficulty": "Intermediate",
        "estimated_hours": 3,
        "prerequisites": ["math_derivatives_gradients"],
        "importance": "How models find optimal weights across complex multi-dimensional loss landscapes.",
        "what_you_will_do": "Compare convex bowls with non-convex landscapes filled with local minima, saddle points, and plateaus.",
        "key_concepts": ["Convex vs non-convex", "Local minima vs global minimum", "Saddle points", "Learning rate steps"]
    },

    # ================= STAGE 3: Data Analysis and Processing =================
    {
        "id": "data_numpy",
        "stage_id": 3,
        "title": "NumPy: High-Performance Vectorized Arrays",
        "difficulty": "Intermediate",
        "estimated_hours": 5,
        "prerequisites": ["py_data_structures", "math_vectors_matrices"],
        "importance": "Replaces slow Python loops with C-optimized SIMD vectorized array calculations (50-100x faster).",
        "what_you_will_do": "Create ndarrays, slice multidimensional arrays, broadcast shapes, and perform vectorized element-wise math.",
        "key_concepts": ["ndarray", "Broadcasting rules", "Array slicing", "Vectorization vs for-loops", "Matrix multiplication (@)"]
    },
    {
        "id": "data_pandas",
        "stage_id": 3,
        "title": "Pandas: DataFrames and Series",
        "difficulty": "Intermediate",
        "estimated_hours": 6,
        "prerequisites": ["data_numpy"],
        "importance": "The core tool for loading, transforming, filtering, and aggregating tabular datasets.",
        "what_you_will_do": "Load CSV/Parquet files, inspect summary statistics, filter rows with boolean indexing, and perform groupby aggregations.",
        "key_concepts": ["DataFrame & Series", "loc vs iloc", "Filtering & Boolean indexing", "groupby and aggregate", "merge & join"]
    },
    {
        "id": "data_cleaning",
        "stage_id": 3,
        "title": "Data Cleaning: Missing Values, Duplicates, and Outliers",
        "difficulty": "Intermediate",
        "estimated_hours": 4,
        "prerequisites": ["data_pandas"],
        "importance": "Garbage in, garbage out. Real-world datasets are riddled with nulls, duplicates, and sensory glitches.",
        "what_you_will_do": "Detect null values, choose appropriate imputation strategies (mean, median, forward fill), remove duplicates, and detect outliers with IQR/Z-score.",
        "key_concepts": ["isna / fillna / dropna", "Duplicate record removal", "IQR (Interquartile Range)", "Z-score outlier thresholding"]
    },
    {
        "id": "data_matplotlib",
        "stage_id": 3,
        "title": "Data Visualization: Matplotlib & Seaborn",
        "difficulty": "Intermediate",
        "estimated_hours": 4,
        "prerequisites": ["data_pandas"],
        "importance": "Seeing patterns, distributions, and anomalies visually prevents wasted modeling cycles.",
        "what_you_will_do": "Plot histograms, scatter plots, correlation heatmaps, box plots, and loss curves with custom formatting.",
        "key_concepts": ["Figures and Axes", "Histograms & KDE", "Scatter plots", "Correlation heatmaps", "Subplots"]
    },
    {
        "id": "data_eda",
        "stage_id": 3,
        "title": "Exploratory Data Analysis (EDA)",
        "difficulty": "Intermediate",
        "estimated_hours": 4,
        "prerequisites": ["data_cleaning", "data_matplotlib"],
        "importance": "Uncovering the underlying story and feature relationships before selecting a model.",
        "what_you_will_do": "Systematically analyze target variable distribution, compute feature correlations, check class balance, and formulate hypotheses.",
        "key_concepts": ["Univariate analysis", "Bivariate analysis", "Skewness & Kurtosis", "Correlation matrices"]
    },
    {
        "id": "data_encoding",
        "stage_id": 3,
        "title": "Categorical Encoding and Feature Scaling",
        "difficulty": "Intermediate",
        "estimated_hours": 4,
        "prerequisites": ["data_eda"],
        "importance": "ML algorithms only understand numbers. Unscaled features cause gradient descent to oscillate wildly.",
        "what_you_will_do": "Apply One-Hot Encoding, Ordinal Encoding, StandardScaler, and MinMaxScaler without introducing data leakage.",
        "key_concepts": ["One-Hot Encoding", "Label/Ordinal Encoding", "StandardScaler (Z-score)", "MinMaxScaler (0-1)"]
    },
    {
        "id": "data_leakage",
        "stage_id": 3,
        "title": "Data Leakage and Train/Val/Test Splits",
        "difficulty": "Intermediate+",
        "estimated_hours": 3,
        "prerequisites": ["data_encoding"],
        "importance": "Preventing overly optimistic benchmark scores that crash and fail when deployed to production.",
        "what_you_will_do": "Perform stratified train/test splits, fit scalers exclusively on the training set, and diagnose lookahead bias.",
        "key_concepts": ["Train vs Validation vs Test", "Stratified splitting", "Fitting scalers on train only", "Temporal leakage"]
    },
    {
        "id": "data_sql",
        "stage_id": 3,
        "title": "SQL Fundamentals for Data Extraction",
        "difficulty": "Intermediate",
        "estimated_hours": 4,
        "prerequisites": ["py_syntax"],
        "importance": "Most company training data resides in SQL databases, not clean local CSV files.",
        "what_you_will_do": "Write SELECT, WHERE, JOIN, GROUP BY, HAVING, and window queries to extract clean feature sets directly from relational tables.",
        "key_concepts": ["SELECT & WHERE", "INNER / LEFT / RIGHT JOIN", "GROUP BY & HAVING", "Window functions (ROW_NUMBER)"]
    },

    # ================= STAGE 4: Machine Learning =================
    {
        "id": "ml_foundations",
        "stage_id": 4,
        "title": "Machine Learning Paradigms: Supervised vs Unsupervised",
        "difficulty": "Beginner+",
        "estimated_hours": 3,
        "prerequisites": ["data_eda"],
        "importance": "Knowing when to frame a problem as regression, classification, clustering, or reinforcement learning.",
        "what_you_will_do": "Classify real-world business problems into appropriate machine learning paradigms and define features vs labels.",
        "key_concepts": ["Supervised learning (labels)", "Unsupervised learning (patterns)", "Reinforcement learning (rewards)", "Features (X) and Target (y)"]
    },
    {
        "id": "ml_linear_regression",
        "stage_id": 4,
        "title": "Linear Regression and Cost Functions",
        "difficulty": "Intermediate",
        "estimated_hours": 4,
        "prerequisites": ["ml_foundations", "math_derivatives_gradients"],
        "importance": "The foundational supervised algorithm predicting continuous numerical outcomes.",
        "what_you_will_do": "Derive y = wx + b, calculate Mean Squared Error (MSE), and observe how coefficients represent feature impact.",
        "key_concepts": ["Weights and Bias", "Mean Squared Error (MSE)", "Residuals", "R-squared metric"]
    },
    {
        "id": "ml_gradient_descent",
        "stage_id": 4,
        "title": "Gradient Descent (Batch, Mini-batch, Stochastic)",
        "difficulty": "Intermediate",
        "estimated_hours": 4,
        "prerequisites": ["ml_linear_regression", "math_optimization"],
        "importance": "The algorithm that iteratively updates model weights to minimize the loss function.",
        "what_you_will_do": "Implement Gradient Descent step updates, tune learning rates, and compare Batch vs Stochastic vs Mini-batch iterations.",
        "key_concepts": ["Weight update formula: w = w - lr * grad", "Learning rate selection", "Batch vs Mini-batch vs SGD", "Convergence"]
    },
    {
        "id": "ml_logistic_regression",
        "stage_id": 4,
        "title": "Logistic Regression and Binary Classification",
        "difficulty": "Intermediate",
        "estimated_hours": 4,
        "prerequisites": ["ml_gradient_descent", "math_probability"],
        "importance": "Predicting probabilities of discrete classes (spam/not spam, disease/healthy).",
        "what_you_will_do": "Pass linear outputs through the Sigmoid function, compute Binary Cross-Entropy loss, and set decision thresholds.",
        "key_concepts": ["Sigmoid function", "Log-odds", "Binary Cross-Entropy (Log Loss)", "Decision threshold tuning (0.5 vs custom)"]
    },
    {
        "id": "ml_eval_metrics",
        "stage_id": 4,
        "title": "Evaluation Metrics: Confusion Matrix, Precision, Recall, F1",
        "difficulty": "Intermediate",
        "estimated_hours": 4,
        "prerequisites": ["ml_logistic_regression"],
        "importance": "Accuracy is misleading on imbalanced datasets (e.g. 99% fraud detection accuracy is useless if it misses all fraud).",
        "what_you_will_do": "Construct confusion matrices, compute Precision, Recall, F1-Score, and plot ROC-AUC curves.",
        "key_concepts": ["True Positives, False Positives", "Precision vs Recall trade-off", "F1-score", "ROC-AUC curve", "Class imbalance"]
    },
    {
        "id": "ml_trees_forests",
        "stage_id": 4,
        "title": "Decision Trees and Random Forests",
        "difficulty": "Intermediate",
        "estimated_hours": 5,
        "prerequisites": ["ml_eval_metrics"],
        "importance": "Ensemble tree methods remain top performers for non-linear tabular business data.",
        "what_you_will_do": "Understand Gini impurity / information gain splits, build single decision trees, and ensemble them via bagging in Random Forests.",
        "key_concepts": ["Decision tree nodes & splits", "Gini impurity & Entropy", "Bagging (Bootstrap Aggregation)", "Random Forests & feature subsampling"]
    },
    {
        "id": "ml_gradient_boosting",
        "stage_id": 4,
        "title": "Gradient Boosting (XGBoost, LightGBM, CatBoost)",
        "difficulty": "Intermediate+",
        "estimated_hours": 5,
        "prerequisites": ["ml_trees_forests"],
        "importance": "The gold standard competition and industry benchmark for tabular data.",
        "what_you_will_do": "Train trees sequentially on the residual errors of preceding trees, tune learning rate shrinkage, and benchmark performance.",
        "key_concepts": ["Sequential boosting", "Residual fitting", "XGBoost & LightGBM", "Early stopping"]
    },
    {
        "id": "ml_regularization",
        "stage_id": 4,
        "title": "Overfitting, Underfitting, and Regularization (L1/L2)",
        "difficulty": "Intermediate+",
        "estimated_hours": 4,
        "prerequisites": ["ml_gradient_descent"],
        "importance": "Ensures the model generalizes to unseen test data instead of merely memorizing training samples.",
        "what_you_will_do": "Diagnose the Bias-Variance tradeoff, apply L1 Lasso (feature selection) and L2 Ridge (weight shrinkage) penalties.",
        "key_concepts": ["Bias-Variance tradeoff", "L1 Lasso regularization", "L2 Ridge regularization", "ElasticNet"]
    },
    {
        "id": "ml_naive_bayes",
        "stage_id": 4,
        "title": "Naive Bayes & Support Vector Machines",
        "difficulty": "Intermediate",
        "estimated_hours": 3,
        "prerequisites": ["ml_eval_metrics", "math_probability"],
        "importance": "Lightweight, blazingly fast baseline models for text and high-dimensional spaces.",
        "what_you_will_do": "Train Multinomial Naive Bayes for text classification and understand SVM maximum-margin hyperplanes.",
        "key_concepts": ["Conditional independence assumption", "MultinomialNB", "Maximum margin hyperplane", "Kernel trick"]
    },
    {
        "id": "ml_kmeans",
        "stage_id": 4,
        "title": "K-Means Clustering and Unsupervised Grouping",
        "difficulty": "Intermediate",
        "estimated_hours": 3,
        "prerequisites": ["data_numpy", "math_dot_products"],
        "importance": "Discovering hidden segments in user bases, customer profiles, and product catalogues.",
        "what_you_will_do": "Iterate cluster centroids, compute inertia, evaluate the Elbow method, and assess Silhouette scores.",
        "key_concepts": ["Cluster centroids", "Inertia (Within-cluster sum of squares)", "Elbow curve", "Silhouette coefficient"]
    },
    {
        "id": "ml_pca",
        "stage_id": 4,
        "title": "Dimensionality Reduction: PCA",
        "difficulty": "Intermediate+",
        "estimated_hours": 4,
        "prerequisites": ["math_vectors_matrices", "data_numpy"],
        "importance": "Compress hundreds of features into a few principal components while preserving maximum variance.",
        "what_you_will_do": "Compute covariance matrices, extract eigenvectors/eigenvalues, and project high-dimensional data onto 2D/3D visualizations.",
        "key_concepts": ["Principal components", "Explained variance ratio", "Eigenvalues & Eigenvectors", "Data compression"]
    },
    {
        "id": "ml_sklearn_pipelines",
        "stage_id": 4,
        "title": "Scikit-Learn Pipelines & Hyperparameter Tuning",
        "difficulty": "Intermediate+",
        "estimated_hours": 4,
        "prerequisites": ["data_leakage", "ml_trees_forests"],
        "importance": "Packaging end-to-end preprocessing, scaling, and modeling into a clean, reproducible object.",
        "what_you_will_do": "Build `Pipeline` and `ColumnTransformer` objects, perform K-Fold Cross Validation, and search hyperparameters with GridSearchCV.",
        "key_concepts": ["Pipeline & ColumnTransformer", "K-Fold Cross Validation", "GridSearchCV vs RandomizedSearchCV", "Serialization (joblib)"]
    },

    # ================= STAGE 5: Deep Learning =================
    {
        "id": "dl_neurons",
        "stage_id": 5,
        "title": "Artificial Neurons, Perceptrons, and Activation Functions",
        "difficulty": "Intermediate",
        "estimated_hours": 4,
        "prerequisites": ["ml_logistic_regression"],
        "importance": "The atomic computational unit of all deep neural networks.",
        "what_you_will_do": "Compute z = W·X + b and apply non-linear activations: ReLU, Sigmoid, Tanh, and LeakyReLU.",
        "key_concepts": ["Perceptron", "Why non-linearity is required", "ReLU and dead ReLU", "GELU & Swish"]
    },
    {
        "id": "dl_forward_prop",
        "stage_id": 5,
        "title": "Multilayer Perceptrons & Forward Propagation",
        "difficulty": "Intermediate+",
        "estimated_hours": 4,
        "prerequisites": ["dl_neurons"],
        "importance": "How signals and representations flow layer-by-layer from raw inputs to predictions.",
        "what_you_will_do": "Trace tensor shapes through input, hidden, and output layers with matrix multiplications.",
        "key_concepts": ["Input, Hidden, Output layers", "Dense / Linear layers", "Tensor dimensional transformations", "Logits"]
    },
    {
        "id": "dl_backprop",
        "stage_id": 5,
        "title": "Backpropagation & Autograd Intuition",
        "difficulty": "Advanced",
        "estimated_hours": 5,
        "prerequisites": ["dl_forward_prop", "math_chain_rule"],
        "importance": "How errors flow backwards through layers to calculate partial derivatives with respect to every weight.",
        "what_you_will_do": "Trace gradient calculations layer by layer and see how automatic differentiation (autograd) tracks the computational graph.",
        "key_concepts": ["Loss function", "Backward pass", "Chain rule in tensors", "Vanishing & exploding gradients"]
    },
    {
        "id": "dl_optimizers",
        "stage_id": 5,
        "title": "Optimizers: SGD, Momentum, Adam, AdamW",
        "difficulty": "Intermediate+",
        "estimated_hours": 4,
        "prerequisites": ["dl_backprop"],
        "importance": "Modern optimizers like AdamW accelerate convergence and prevent getting stuck in local traps.",
        "what_you_will_do": "Compare pure SGD, SGD with Momentum, RMSprop, and Adam's adaptive learning rates with decoupled weight decay.",
        "key_concepts": ["Momentum (rolling velocity)", "Adaptive learning rates (Adam)", "Decoupled weight decay (AdamW)", "Learning rate warmups"]
    },
    {
        "id": "dl_regularization",
        "stage_id": 5,
        "title": "Deep Learning Regularization: Dropout & Batch Normalization",
        "difficulty": "Intermediate+",
        "estimated_hours": 4,
        "prerequisites": ["dl_optimizers"],
        "importance": "Prevents billion-parameter networks from overfitting and stabilizes intermediate layer distributions.",
        "what_you_will_do": "Implement Dropout masks during training, evaluate eval mode behavior, and apply LayerNorm / BatchNorm.",
        "key_concepts": ["Dropout (random co-adaptation breaking)", "Batch Normalization vs Layer Normalization", "train() vs eval() mode in PyTorch"]
    },
    {
        "id": "dl_pytorch_tensors",
        "stage_id": 5,
        "title": "PyTorch Fundamentals: Tensors & GPU Acceleration",
        "difficulty": "Intermediate+",
        "estimated_hours": 5,
        "prerequisites": ["data_numpy", "py_oop"],
        "importance": "PyTorch is the undisputed primary research and production framework for AI engineers.",
        "what_you_will_do": "Create PyTorch tensors, handle GPU device transfers (`.to('cuda')`), and manage tensor memory and autograd flags.",
        "key_concepts": ["torch.Tensor", "requires_grad=True", "CUDA device allocation", "Tensor reshape / view / permute"]
    },
    {
        "id": "dl_training_loop",
        "stage_id": 5,
        "title": "PyTorch Dataset, DataLoader, and Training Loops",
        "difficulty": "Advanced",
        "estimated_hours": 6,
        "prerequisites": ["dl_pytorch_tensors", "dl_backprop"],
        "importance": "The universal recipe for training neural models in industry.",
        "what_you_will_do": "Write custom Dataset classes with `__len__` and `__getitem__`, configure multi-worker DataLoaders, and code the standard 5-step training loop.",
        "key_concepts": ["Custom Dataset", "DataLoader & batching", "zero_grad() -> backward() -> step()", "Model checkpointing"]
    },

    # ================= STAGE 6: Specialized Neural Networks =================
    {
        "id": "snn_cnn",
        "stage_id": 6,
        "title": "Convolutional Neural Networks (CNNs)",
        "difficulty": "Intermediate+",
        "estimated_hours": 5,
        "prerequisites": ["dl_training_loop"],
        "importance": "The backbone of computer vision: spatial feature extractors with translation invariance.",
        "what_you_will_do": "Apply convolutional kernels, pooling layers, calculate output feature map dimensions, and build vision classifiers.",
        "key_concepts": ["Convolutional kernels/filters", "Stride and Padding", "Max Pooling", "Feature hierarchy (edges -> textures -> objects)"]
    },
    {
        "id": "snn_transfer_learning",
        "stage_id": 6,
        "title": "Transfer Learning & Fine-Tuning Vision Models",
        "difficulty": "Advanced",
        "estimated_hours": 5,
        "prerequisites": ["snn_cnn"],
        "importance": "Nobody trains vision models from scratch anymore; transfer learning yields state-of-the-art results with tiny datasets.",
        "what_you_will_do": "Load pretrained ResNet or Vision Transformer backbones, freeze early layers, and train a new classification head.",
        "key_concepts": ["Pretrained backbones (ImageNet)", "Freezing weights (`param.requires_grad = False`)", "Fine-tuning head", "Differential learning rates"]
    },
    {
        "id": "snn_embeddings",
        "stage_id": 6,
        "title": "Embeddings: Mapping Meaning to Vectors",
        "difficulty": "Intermediate+",
        "estimated_hours": 4,
        "prerequisites": ["math_dot_products", "dl_pytorch_tensors"],
        "importance": "Transforms discrete tokens, words, or images into continuous vector spaces where semantic similarity equals geometric proximity.",
        "what_you_will_do": "Train Word2Vec embeddings or inspect pretrained vector spaces where King - Man + Woman ≈ Queen.",
        "key_concepts": ["Vector space semantics", "Cosine similarity in embeddings", "Word2Vec (Skip-gram, CBOW)", "Embedding layers (`nn.Embedding`)"]
    },
    {
        "id": "snn_attention",
        "stage_id": 6,
        "title": "Attention Mechanism Intuition",
        "difficulty": "Advanced",
        "estimated_hours": 5,
        "prerequisites": ["snn_embeddings", "math_dot_products"],
        "importance": "The breakthrough that solved the bottleneck of fixed-length recurrent states and catalyzed modern LLMs.",
        "what_you_will_do": "Visualize dynamic weighting across sequence elements so each word pays attention to relevant context.",
        "key_concepts": ["Sequence alignment", "Softmax attention weights", "Context vectors", "Why recurrent networks failed on long sequences"]
    },
    {
        "id": "snn_transformers",
        "stage_id": 6,
        "title": "The Transformer Architecture: Attention Is All You Need",
        "difficulty": "Advanced",
        "estimated_hours": 6,
        "prerequisites": ["snn_attention"],
        "importance": "The dominant architecture powering GPT-4, Claude, Gemini, Llama, and modern vision systems.",
        "what_you_will_do": "Deconstruct the complete Transformer diagram: Positional Encoding, Multi-Head Attention, Feed-Forward layers, and Residual connections.",
        "key_concepts": ["Encoder vs Decoder", "Positional Encodings", "Residual connections & LayerNorm", "Feed-Forward sub-layers"]
    },
    {
        "id": "snn_qkv",
        "stage_id": 6,
        "title": "Query, Key, and Value (Q, K, V) Deep Dive",
        "difficulty": "Advanced",
        "estimated_hours": 5,
        "prerequisites": ["snn_transformers"],
        "importance": "The core mathematical operation inside every Transformer block: Attention(Q, K, V) = softmax(QK^T / sqrt(d_k))V.",
        "what_you_will_do": "Trace Query vectors searching Key registries to extract weighted Value representations with matrix operations.",
        "key_concepts": ["Query (what I'm looking for)", "Key (what I offer)", "Value (what content I provide)", "Scaled dot-product attention formula"]
    },

    # ================= STAGE 7: NLP and LLMs =================
    {
        "id": "llm_tokenization",
        "stage_id": 7,
        "title": "Tokenization, Vocabularies, and Token IDs",
        "difficulty": "Intermediate+",
        "estimated_hours": 4,
        "prerequisites": ["py_strings", "snn_embeddings"],
        "importance": "LLMs do not read words; they process numerical token IDs generated by Byte-Pair Encoding (BPE).",
        "what_you_will_do": "Use tokenizers (TikToken, HuggingFace), inspect subword splits, calculate token count costs, and debug tokenization anomalies.",
        "key_concepts": ["Byte-Pair Encoding (BPE)", "Vocabulary size", "Token-to-word ratio", "Special tokens (<|endoftext|>)"]
    },
    {
        "id": "llm_context_windows",
        "stage_id": 7,
        "title": "LLM Fundamentals: Context Windows, Sampling, Temperature",
        "difficulty": "Intermediate",
        "estimated_hours": 4,
        "prerequisites": ["llm_tokenization"],
        "importance": "Controlling the creativity, determinism, and capacity of language models in production.",
        "what_you_will_do": "Control model outputs using Temperature, Top-P (nucleus sampling), Top-K, and frequency/presence penalties.",
        "key_concepts": ["Context window length", "Temperature (0.0 deterministic vs 1.0 creative)", "Top-P nucleus sampling", "Logits to probabilities"]
    },
    {
        "id": "llm_prompt_engineering",
        "stage_id": 7,
        "title": "Prompt Engineering: Zero-Shot, Few-Shot, and CoT",
        "difficulty": "Intermediate",
        "estimated_hours": 4,
        "prerequisites": ["llm_context_windows"],
        "importance": "Extracting high-precision reasoning and reliable behavior from pre-trained frontier models without fine-tuning.",
        "what_you_will_do": "Design system vs user prompts, provide few-shot exemplar formatting, and trigger Chain-of-Thought (CoT) reasoning.",
        "key_concepts": ["System instructions", "Few-shot prompting", "Chain-of-Thought (CoT)", "Role prompting & output delimiters"]
    },
    {
        "id": "llm_structured_outputs",
        "stage_id": 7,
        "title": "Structured Outputs and Schema Validation (Pydantic / JSON Mode)",
        "difficulty": "Intermediate+",
        "estimated_hours": 5,
        "prerequisites": ["llm_prompt_engineering", "py_oop"],
        "importance": "AI engineering requires strict programmatically parseable JSON, not conversational prose.",
        "what_you_will_do": "Enforce strict JSON schema generation using Pydantic models, JSON Mode, and tool schema validation.",
        "key_concepts": ["JSON Mode", "Pydantic schema constraints", "Grammar-based constrained decoding", "Parse failure retry loops"]
    },
    {
        "id": "llm_hallucinations",
        "stage_id": 7,
        "title": "Hallucinations and Factual Verification",
        "difficulty": "Intermediate+",
        "estimated_hours": 4,
        "prerequisites": ["llm_prompt_engineering"],
        "importance": "Mitigating the fundamental risk of generative models fabricating plausible-sounding falsehoods.",
        "what_you_will_do": "Detect hallucination triggers, benchmark factual consistency, and design ground-truth verification loops.",
        "key_concepts": ["Why LLMs hallucinate", "Extrinsic vs Intrinsic hallucinations", "Factual consistency scoring", "Groundedness checks"]
    },
    {
        "id": "llm_api_integration",
        "stage_id": 7,
        "title": "API Integration, Streaming Responses, and Latency Optimization",
        "difficulty": "Intermediate+",
        "estimated_hours": 5,
        "prerequisites": ["llm_structured_outputs", "py_errors"],
        "importance": "Integrating enterprise AI APIs into production applications with pleasant user experiences.",
        "what_you_will_do": "Implement Server-Sent Events (SSE) streaming for instant token-by-token UI updates, exponential backoff, and token budgeting.",
        "key_concepts": ["Streaming / Server-Sent Events (SSE)", "Time-to-First-Token (TTFT)", "Exponential backoff & jitter", "Token rate limits (TPM / RPM)"]
    },

    # ================= STAGE 8: RAG =================
    {
        "id": "rag_foundations",
        "stage_id": 8,
        "title": "What RAG Solves: Knowledge Cutoffs and Private Data",
        "difficulty": "Intermediate",
        "estimated_hours": 3,
        "prerequisites": ["llm_prompt_engineering"],
        "importance": "Enables models to accurately answer questions about internal company docs without expensive fine-tuning.",
        "what_you_will_do": "Diagram the complete RAG architecture: Ingestion -> Chunking -> Embedding -> Storage -> Retrieval -> Generation.",
        "key_concepts": ["Parametric vs Non-parametric memory", "Knowledge cutoffs", "Private enterprise data isolation", "Hallucination reduction"]
    },
    {
        "id": "rag_chunking",
        "stage_id": 8,
        "title": "Document Parsing and Chunking Strategies",
        "difficulty": "Intermediate+",
        "estimated_hours": 4,
        "prerequisites": ["rag_foundations", "py_strings"],
        "importance": "Bad chunks destroy retrieval quality. The chunk is the atomic unit of retrieved context.",
        "what_you_will_do": "Implement fixed-size chunking with overlaps, recursive character chunking, semantic chunking, and markdown header awareness.",
        "key_concepts": ["Chunk size vs Chunk overlap", "Recursive character splitting", "Semantic boundary splitting", "Preserving tables and headers"]
    },
    {
        "id": "rag_embeddings",
        "stage_id": 8,
        "title": "Embedding Models and Vector Similarity Search",
        "difficulty": "Intermediate+",
        "estimated_hours": 4,
        "prerequisites": ["rag_chunking", "snn_embeddings"],
        "importance": "Selecting the right text embedding model to convert document passages into searchable coordinates.",
        "what_you_will_do": "Generate dense vector embeddings, normalize vectors, and compute cosine similarity queries across document collections.",
        "key_concepts": ["Dense retrieval", "MTEB Leaderboard", "Cosine similarity vs Dot product vs Euclidean distance", "Vector normalization"]
    },
    {
        "id": "rag_vector_db",
        "stage_id": 8,
        "title": "Vector Databases and Indexing (ANN, HNSW)",
        "difficulty": "Advanced",
        "estimated_hours": 5,
        "prerequisites": ["rag_embeddings"],
        "importance": "Searching millions of vectors in milliseconds requires specialized Approximate Nearest Neighbor (ANN) indexes.",
        "what_you_will_do": "Work with vector stores (Chroma, Pinecone, Qdrant, pgvector), build HNSW graph indexes, and perform metadata filtering.",
        "key_concepts": ["Exact KNN vs Approximate Nearest Neighbor (ANN)", "HNSW (Hierarchical Navigable Small World)", "Metadata filtering", "pgvector"]
    },
    {
        "id": "rag_hybrid_search",
        "stage_id": 8,
        "title": "Hybrid Search: Combining BM25 Keyword & Dense Vectors",
        "difficulty": "Advanced",
        "estimated_hours": 4,
        "prerequisites": ["rag_vector_db"],
        "importance": "Pure vector search fails on acronyms, part numbers, and exact product names; hybrid search fixes this.",
        "what_you_will_do": "Implement sparse BM25 scoring alongside dense vector queries and fuse results using Reciprocal Rank Fusion (RRF).",
        "key_concepts": ["Sparse retrieval (BM25)", "Dense retrieval", "Reciprocal Rank Fusion (RRF)", "Alpha weighting"]
    },
    {
        "id": "rag_reranking",
        "stage_id": 8,
        "title": "Cross-Encoder Reranking and Context Compression",
        "difficulty": "Advanced",
        "estimated_hours": 4,
        "prerequisites": ["rag_hybrid_search"],
        "importance": "Bi-encoders are fast for initial retrieval (top-50), but cross-encoders provide superior accuracy for top-3 context ranking.",
        "what_you_will_do": "Pass query-document pairs through a cross-encoder model (Cohere Rerank / BGE Reranker) and re-order the retrieved candidates.",
        "key_concepts": ["Bi-Encoder vs Cross-Encoder", "Reranker models", "Context compression", "Lost-in-the-middle phenomenon"]
    },
    {
        "id": "rag_grounded_gen",
        "stage_id": 8,
        "title": "Grounded Generation and Citations Attribution",
        "difficulty": "Advanced",
        "estimated_hours": 4,
        "prerequisites": ["rag_reranking", "llm_structured_outputs"],
        "importance": "Giving users complete trust by linking every statement directly to clickable source documents and page numbers.",
        "what_you_will_do": "Format prompt context blocks with unique reference IDs and instruct the model to produce strict markdown citations.",
        "key_concepts": ["System context formatting", "In-line citations ([1], [2])", "Fallback when information is not in context", "Source transparency"]
    },
    {
        "id": "rag_evaluation",
        "stage_id": 8,
        "title": "RAG Evaluation: Faithfulness and Answer Relevance (Ragas)",
        "difficulty": "Advanced",
        "estimated_hours": 4,
        "prerequisites": ["rag_grounded_gen"],
        "importance": "You cannot improve what you cannot measure; evaluating RAG requires measuring retrieval and generation separately.",
        "what_you_will_do": "Measure Context Precision, Context Recall, Faithfulness (hallucination-free), and Answer Relevance using the RAG triad.",
        "key_concepts": ["The RAG Triad", "Faithfulness (no made-up facts)", "Answer Relevance", "Context Recall", "Synthetic test dataset generation"]
    },

    # ================= STAGE 9: AI Agents =================
    {
        "id": "agent_foundations",
        "stage_id": 9,
        "title": "Agent Architectures: Chatbots vs Autonomous Agents",
        "difficulty": "Intermediate+",
        "estimated_hours": 3,
        "prerequisites": ["llm_api_integration"],
        "importance": "Understanding the fundamental leap from passive conversational responders to autonomous goal-directed systems.",
        "what_you_will_do": "Diagram the core agent loop: Observe -> Think / Plan -> Act (Call Tool) -> Observe Feedback -> Finish.",
        "key_concepts": ["Passive LLM vs Active Agent", "The ReAct loop (Reason + Act)", "Environment feedback", "Autonomous termination criteria"]
    },
    {
        "id": "agent_tools_calling",
        "stage_id": 9,
        "title": "Tools and Function Calling",
        "difficulty": "Advanced",
        "estimated_hours": 5,
        "prerequisites": ["agent_foundations", "llm_structured_outputs"],
        "importance": "Empowers models to execute code, search the web, query databases, and call external APIs.",
        "what_you_will_do": "Define strict JSON tool schemas, handle model tool-call decisions, execute the local function, and return tool outputs.",
        "key_concepts": ["Tool schema definitions", "Tool calling protocol", "Execution sandbox", "Returning tool results to conversation"]
    },
    {
        "id": "agent_state_memory",
        "stage_id": 9,
        "title": "Agent State and Memory Systems",
        "difficulty": "Advanced",
        "estimated_hours": 4,
        "prerequisites": ["agent_tools_calling"],
        "importance": "Enables agents to remember context across long multi-turn workflows and retain key user preferences.",
        "what_you_will_do": "Build short-term conversational buffers, semantic long-term vector memory, and structured state graphs.",
        "key_concepts": ["Short-term working memory", "Long-term episodic memory", "State machines & checkpoints", "Compaction & summarization"]
    },
    {
        "id": "agent_planning",
        "stage_id": 9,
        "title": "Planning and Task Decomposition",
        "difficulty": "Advanced",
        "estimated_hours": 5,
        "prerequisites": ["agent_state_memory"],
        "importance": "Prevents agents from getting stuck in infinite loops or hallucinating execution paths on complex tasks.",
        "what_you_will_do": "Implement Plan-and-Solve patterns, hierarchical task decomposition, dynamic replanning on tool errors, and self-reflection.",
        "key_concepts": ["Task decomposition", "Plan-and-Solve pattern", "Self-reflection & error correction", "Loop detection & cycle limits"]
    },
    {
        "id": "agent_human_approval",
        "stage_id": 9,
        "title": "Human-in-the-Loop & Approval Workflows",
        "difficulty": "Advanced",
        "estimated_hours": 4,
        "prerequisites": ["agent_planning"],
        "importance": "Destructive actions (sending emails, modifying databases, making payments) must require human confirmation.",
        "what_you_will_do": "Build pause-and-resume workflows where high-stakes tool calls generate an approval ticket awaiting user signature.",
        "key_concepts": ["Read-only vs Side-effect tools", "Approval gates", "State suspension and resumption", "Audit logs"]
    },
    {
        "id": "agent_guardrails",
        "stage_id": 9,
        "title": "Agent Guardrails and When NOT to Use Agents",
        "difficulty": "Advanced",
        "estimated_hours": 3,
        "prerequisites": ["agent_human_approval"],
        "importance": "Choosing deterministic code over non-deterministic agents when reliability, latency, and cost matter.",
        "what_you_will_do": "Evaluate deterministic code vs autonomous agents, and apply safety boundaries to contain agent permissions.",
        "key_concepts": ["Deterministic workflows vs autonomous agents", "Rate limits & recursion depth limits", "Permission scoping", "Cost explosion defense"]
    },

    # ================= STAGE 10: Backend Development =================
    {
        "id": "be_fastapi",
        "stage_id": 10,
        "title": "FastAPI & REST APIs for AI Services",
        "difficulty": "Intermediate+",
        "estimated_hours": 5,
        "prerequisites": ["py_oop", "py_errors"],
        "importance": "FastAPI is the industry standard Python framework for serving high-performance machine learning APIs.",
        "what_you_will_do": "Build REST endpoints (GET, POST), handle path and query parameters, and auto-generate OpenAPI documentation.",
        "key_concepts": ["FastAPI routing", "Request/Response lifecycle", "HTTP status codes", "Interactive Swagger docs"]
    },
    {
        "id": "be_pydantic",
        "stage_id": 10,
        "title": "Pydantic & Request/Response Validation",
        "difficulty": "Intermediate+",
        "estimated_hours": 4,
        "prerequisites": ["be_fastapi"],
        "importance": "Guarantees type-safety, input sanitation, and automated error responses before requests touch your AI models.",
        "what_you_will_do": "Define Pydantic schemas, add custom validators, regex patterns, and nested data representations.",
        "key_concepts": ["BaseModel", "Field validation & constraints", "Custom @field_validator", "Serialization with model_dump()"]
    },
    {
        "id": "be_async",
        "stage_id": 10,
        "title": "Asynchronous Programming (async/await) in Python",
        "difficulty": "Advanced",
        "estimated_hours": 4,
        "prerequisites": ["be_fastapi"],
        "importance": "AI APIs spend most of their time waiting on external network I/O; async handles thousands of concurrent requests without blocking.",
        "what_you_will_do": "Write async/await coroutines, manage event loops, and execute concurrent calls with `asyncio.gather`.",
        "key_concepts": ["Event loop", "async def & await", "Non-blocking I/O", "asyncio.gather()", "Thread pools for CPU-bound tasks"]
    },
    {
        "id": "be_docker",
        "stage_id": 10,
        "title": "Docker Containerization for AI Applications",
        "difficulty": "Intermediate+",
        "estimated_hours": 5,
        "prerequisites": ["py_terminal", "py_virtual_envs"],
        "importance": "Packages system libraries, Python packages, CUDA drivers, and code into an immutable, portable container.",
        "what_you_will_do": "Write multi-stage Dockerfiles, minimize image sizes, set non-root users, and run containers with volume mounts.",
        "key_concepts": ["Dockerfile instructions", "Image layers & caching", "Multi-stage builds", "Docker Compose", "Environment variables"]
    },

    # ================= STAGE 11: Deployment & MLOps =================
    {
        "id": "ops_model_serving",
        "stage_id": 11,
        "title": "Model Serialization and Serving (ONNX, vLLM)",
        "difficulty": "Advanced",
        "estimated_hours": 5,
        "prerequisites": ["dl_training_loop", "be_docker"],
        "importance": "Raw PyTorch models are unoptimized for production throughput; specialized inference engines provide 5-10x speedups.",
        "what_you_will_do": "Export models to ONNX/Safetensors, understand vLLM continuous batching and PagedAttention, and configure serving runtimes.",
        "key_concepts": ["Safetensors format", "ONNX runtime", "vLLM & PagedAttention", "Continuous batching", "Inference latency (TTFT)"]
    },
    {
        "id": "ops_drift_detection",
        "stage_id": 11,
        "title": "Data Drift, Concept Drift, and Monitoring",
        "difficulty": "Advanced",
        "estimated_hours": 4,
        "prerequisites": ["ml_eval_metrics", "math_probability"],
        "importance": "Real-world data changes over time. Unmonitored models silently decay and cause catastrophic business errors.",
        "what_you_will_do": "Implement Kolmogorov-Smirnov and PSI (Population Stability Index) tests to detect feature distribution shifts.",
        "key_concepts": ["Data drift vs Concept drift", "Population Stability Index (PSI)", "Statistical hypothesis tests (KS-test)", "Retraining triggers"]
    },
    {
        "id": "ops_monitoring",
        "stage_id": 11,
        "title": "Observability: Tracing, Latency, and Cost Tracking",
        "difficulty": "Advanced",
        "estimated_hours": 4,
        "prerequisites": ["ops_model_serving", "llm_api_integration"],
        "importance": "Track token costs, latency bottlenecks, and error rates across multi-step LLM calls.",
        "what_you_will_do": "Set up OpenTelemetry spans, log user prompts and model completions safely, and create cost alert thresholds.",
        "key_concepts": ["Distributed tracing", "Latency percentiles (p50, p95, p99)", "Token spend dashboards", "Anonymization & PII redaction"]
    },

    # ================= STAGE 12: Advanced AI Engineering =================
    {
        "id": "adv_gpu_memory",
        "stage_id": 12,
        "title": "GPU Architecture and Memory-Efficient Inference",
        "difficulty": "Advanced+",
        "estimated_hours": 5,
        "prerequisites": ["dl_pytorch_tensors", "ops_model_serving"],
        "importance": "Fitting large models into limited VRAM without running out of memory (OOM).",
        "what_you_will_do": "Calculate exact VRAM requirements (weights, KV cache, activations), and utilize FlashAttention and FP16/BF16 precision.",
        "key_concepts": ["VRAM breakdown (Weights, KV-Cache, Activations)", "FP32 vs FP16 vs BF16", "FlashAttention memory savings", "CUDA Out-of-Memory (OOM) diagnosis"]
    },
    {
        "id": "adv_quantization",
        "stage_id": 12,
        "title": "Model Quantization (INT8, INT4, AWQ, GGUF)",
        "difficulty": "Advanced+",
        "estimated_hours": 5,
        "prerequisites": ["adv_gpu_memory"],
        "importance": "Run 70B models on commodity hardware by compressing 16-bit floating point weights into 4-bit integers.",
        "what_you_will_do": "Compare Post-Training Quantization (PTQ) vs Quantization-Aware Training (QAT), and benchmark GGUF and AWQ models.",
        "key_concepts": ["Post-Training Quantization (PTQ)", "INT8 vs INT4 precision", "AWQ & GPTQ", "GGUF for local CPU/Metal inference"]
    },
    {
        "id": "adv_lora_peft",
        "stage_id": 12,
        "title": "Fine-Tuning with LoRA & Parameter-Efficient Adaptation",
        "difficulty": "Master",
        "estimated_hours": 6,
        "prerequisites": ["dl_backprop", "snn_transformers", "adv_gpu_memory"],
        "importance": "Fine-tune 7B-70B models on a single consumer GPU by training tiny low-rank adapter matrices instead of full weights.",
        "what_you_will_do": "Configure LoRA rank (r) and alpha, attach adapter weights to Transformer linear projection layers, and merge adapters.",
        "key_concepts": ["Low-Rank Adaptation (LoRA)", "QLoRA (4-bit base + 16-bit LoRA)", "Rank (r) and Alpha scaling", "Target modules (q_proj, v_proj)"]
    },
    {
        "id": "adv_eval_frameworks",
        "stage_id": 12,
        "title": "Evaluation Frameworks & LLM-as-a-Judge Limitations",
        "difficulty": "Advanced+",
        "estimated_hours": 4,
        "prerequisites": ["llm_hallucinations", "rag_evaluation"],
        "importance": "Automating continuous evaluation while avoiding self-enhancement bias and positional bias in LLM evaluators.",
        "what_you_will_do": "Design pairwise evaluation harnesses, mitigate position and verbosity bias in judge models, and correlate with human scores.",
        "key_concepts": ["LLM-as-a-judge", "Position bias & Verbosity bias", "Pairwise vs Single-score grading", "Golden evaluation benchmark sets"]
    },
    {
        "id": "adv_security_prompt_injection",
        "stage_id": 12,
        "title": "AI Security: Prompt Injection and Jailbreak Defense",
        "difficulty": "Advanced+",
        "estimated_hours": 4,
        "prerequisites": ["llm_prompt_engineering", "agent_guardrails"],
        "importance": "Direct and indirect prompt injections represent the #1 vulnerability on the OWASP Top 10 for LLM Applications.",
        "what_you_will_do": "Simulate indirect prompt injections from untrusted web pages, test delimiter escaping, and implement input guardrails.",
        "key_concepts": ["Direct prompt injection (jailbreaking)", "Indirect prompt injection (untrusted context)", "System prompt leakage", "Input/Output sanitization guards"]
    },
    {
        "id": "adv_responsible_ai",
        "stage_id": 12,
        "title": "System Design for Enterprise AI Applications",
        "difficulty": "Master",
        "estimated_hours": 6,
        "prerequisites": ["be_fastapi", "rag_grounded_gen", "agent_guardrails", "ops_monitoring"],
        "importance": "Synthesizing all 12 stages into scalable, fault-tolerant, cost-effective enterprise AI architectures.",
        "what_you_will_do": "Design an end-to-end architecture balancing latency SLAs, cost tradeoffs, caching tiers, fallback models, and compliance.",
        "key_concepts": ["Tiered routing (small vs frontier model)", "Semantic response caching", "Cost vs latency vs quality trade-offs", "Disaster recovery & model fallbacks"]
    }
]

def get_topics_by_stage(stage_id: int) -> List[Dict[str, Any]]:
    return [t for t in TOPICS if t["stage_id"] == stage_id]

def get_topic_by_id(topic_id: str) -> Dict[str, Any] | None:
    for t in TOPICS:
        if t["id"] == topic_id:
            return t
    return None

