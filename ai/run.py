#!/usr/bin/env python3
"""
AI Engineer Learning OS - Unified Server Launcher
Starts the backend REST server and serves the responsive frontend single-page app.
Zero external pip dependencies required.
"""

import sys
import os

# Add workspace directory to python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.server import run_server

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port: {sys.argv[1]}, defaulting to 8000")
    run_server(port=port)

