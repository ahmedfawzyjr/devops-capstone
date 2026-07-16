"""
DevOps Capstone - Account REST API Service
Flask application factory with Talisman security headers and CORS.
"""

from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS


def create_app():
    """Application factory with security middleware."""
    app = Flask(__name__)

    # ── Security Headers via Talisman ──────────────────────────────────────
    Talisman(
        app,
        force_https=False,
        strict_transport_security=True,
        content_security_policy=False,
        frame_options="DENY",
    )

    # ── CORS Policy ────────────────────────────────────────────────────────
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )

    return app
