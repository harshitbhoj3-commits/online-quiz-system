"""
Configuration Module for QuizMaster — Online Quiz System
Course: BBAT104 — Fundamentals of Total Quality Management
Academic Session: 2026–27
Student Roll Number: 19
Project Type: Individual Project
Core TQM Goal: Minimize latency during quiz submissions and ensure accurate automatic grading.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)


class Config:
    """Base application configuration."""

    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY", "quizmaster-tqm-session-key-roll19-2026-prod-sec")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 3600 * 4  # 4 hours

    # Database
    DATABASE_PATH = os.environ.get("DATABASE_PATH", str(INSTANCE_DIR / "quiz.db"))

    # System Identification & Academic Metadata
    APP_TITLE = "QuizMaster — Online Quiz System"
    APP_SUBTITLE = "TQM-Driven Educational Assessment Platform"
    COURSE = "BBAT104 — Fundamentals of Total Quality Management"
    ACADEMIC_SESSION = "2026–27"
    STUDENT_ROLL_NUMBER = "19"
    PROJECT_TYPE = "Individual Project"
    CORE_TQM_GOAL = "Minimize latency during quiz submissions and ensure accurate automatic grading"

    # =========================================================================
    # QUALITY GOAL REQUIREMENT (DO NOT GUESS)
    # The student's individual Quality Goal (Q01 - Q20) will be assigned from the
    # course evaluation sheet. Until officially confirmed, this setting remains
    # explicitly configured as pending confirmation.
    # To update once confirmed, set QUALITY_GOAL = "Q05" (or assigned code).
    # =========================================================================
    QUALITY_GOAL = os.environ.get("QUALITY_GOAL", "Q_PENDING_CONFIRMATION")
    QUALITY_GOAL_DESCRIPTION = (
        "Individual quality goal assignment pending official evaluation sheet confirmation. "
        "Modular quality features are independently active and configurable."
    )

    # Modular Quality Feature Flags
    FEATURE_AUDIT_LOGGING = True
    FEATURE_DEFECT_TRACKING = True
    FEATURE_LATENCY_METRICS = True
    FEATURE_ROLE_BASED_ACCESS = True
    FEATURE_INPUT_VALIDATION_STRICT = True
    FEATURE_EXPORT_REPORTS = True
    FEATURE_PARETO_ANALYSIS = True
    FEATURE_FISHBONE_ANALYSIS = True
    FEATURE_FMEA_MATRIX = True
    FEATURE_PDCA_LOG = True

    # CTQ Targets
    TARGET_SUBMISSION_LATENCY_MS = 50.0  # Max acceptable server-side submission latency
    TARGET_GRADING_ACCURACY_PCT = 100.0   # Required grading accuracy
    GRACE_PERIOD_SECONDS = 30             # Network latency buffer before marking attempt timed out


class TestConfig(Config):
    """Configuration for automated tests."""
    TESTING = True
    DATABASE_PATH = ":memory:"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test-secret-key-19"
