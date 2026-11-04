"""
Database Access Layer for QuizMaster — Online Quiz System
Uses SQLite3 with parameterized queries, foreign key enforcement,
row factories, connection pooling within request lifecycle, and transactional integrity.
"""

import sqlite3
from flask import g, current_app
from config import Config


SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('student', 'admin')),
    full_name TEXT NOT NULL,
    roll_number TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quizzes Table
CREATE TABLE IF NOT EXISTS quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    duration_minutes INTEGER NOT NULL DEFAULT 10,
    pass_percentage REAL NOT NULL DEFAULT 40.0,
    is_published INTEGER NOT NULL DEFAULT 0,
    allow_review INTEGER NOT NULL DEFAULT 1,
    shuffle_questions INTEGER NOT NULL DEFAULT 0,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Questions Table (Multiple Choice Questions)
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_option TEXT NOT NULL CHECK(correct_option IN ('A', 'B', 'C', 'D')),
    marks REAL NOT NULL DEFAULT 1.0,
    explanation TEXT,
    order_index INTEGER DEFAULT 0
);

-- Quiz Attempts Table
CREATE TABLE IF NOT EXISTS quiz_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    submitted_at TIMESTAMP,
    score REAL DEFAULT 0.0,
    total_marks REAL DEFAULT 0.0,
    percentage REAL DEFAULT 0.0,
    status TEXT NOT NULL DEFAULT 'in_progress' CHECK(status IN ('in_progress', 'completed', 'timed_out')),
    latency_ms REAL DEFAULT 0.0
);

-- Attempt Answers Table (Stores student choices per attempt)
CREATE TABLE IF NOT EXISTS attempt_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attempt_id INTEGER NOT NULL REFERENCES quiz_attempts(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    selected_option TEXT CHECK(selected_option IN ('A', 'B', 'C', 'D', '')),
    is_correct INTEGER DEFAULT 0,
    marks_awarded REAL DEFAULT 0.0,
    UNIQUE(attempt_id, question_id)
);

-- Audit Logs Table
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    entity_type TEXT,
    entity_id INTEGER,
    details TEXT,
    ip_address TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Defect Logs Table (TQM Checksheet & Pareto Data)
CREATE TABLE IF NOT EXISTS defect_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    defect_code TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    severity TEXT NOT NULL CHECK(severity IN ('Low', 'Medium', 'High', 'Critical')),
    occurrence_count INTEGER DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'Open' CHECK(status IN ('Open', 'In Progress', 'Resolved', 'Closed')),
    root_cause TEXT,
    corrective_action TEXT,
    reported_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

-- Quality Metrics Table (CTQ Tracking)
CREATE TABLE IF NOT EXISTS quality_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_name TEXT UNIQUE NOT NULL,
    target_value REAL NOT NULL,
    observed_value REAL,
    unit TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pass' CHECK(status IN ('Pass', 'Fail', 'Pending')),
    notes TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- FMEA Records Table
CREATE TABLE IF NOT EXISTS fmea_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    process_step TEXT NOT NULL,
    potential_failure_mode TEXT NOT NULL,
    potential_effect TEXT NOT NULL,
    potential_cause TEXT NOT NULL,
    severity INTEGER NOT NULL CHECK(severity BETWEEN 1 AND 10),
    occurrence INTEGER NOT NULL CHECK(occurrence BETWEEN 1 AND 10),
    detection INTEGER NOT NULL CHECK(detection BETWEEN 1 AND 10),
    rpn INTEGER NOT NULL,
    mitigation_action TEXT NOT NULL,
    responsible_role TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Active'
);

-- PDCA Continuous Improvement Records Table
CREATE TABLE IF NOT EXISTS pdca_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cycle_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    plan_text TEXT NOT NULL,
    do_text TEXT NOT NULL,
    check_text TEXT NOT NULL,
    act_text TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Standardized',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for fast query execution and latency minimization
CREATE INDEX IF NOT EXISTS idx_questions_quiz_id ON questions(quiz_id);
CREATE INDEX IF NOT EXISTS idx_attempts_user_id ON quiz_attempts(user_id);
CREATE INDEX IF NOT EXISTS idx_attempts_quiz_id ON quiz_attempts(quiz_id);
CREATE INDEX IF NOT EXISTS idx_attempts_status ON quiz_attempts(status);
CREATE INDEX IF NOT EXISTS idx_answers_attempt_id ON attempt_answers(attempt_id);
CREATE INDEX IF NOT EXISTS idx_answers_question_id ON attempt_answers(question_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_defect_logs_category ON defect_logs(category);
"""


def get_db(db_path=None):
    """
    Get or create an active SQLite database connection for the current Flask context
    or standalone runner.
    """
    if db_path is None:
        try:
            db_path = current_app.config.get("DATABASE_PATH", Config.DATABASE_PATH)
        except RuntimeError:
            db_path = Config.DATABASE_PATH

    # Check if inside Flask request context
    try:
        if "db" not in g:
            g.db = sqlite3.connect(db_path)
            g.db.row_factory = sqlite3.Row
            g.db.execute("PRAGMA foreign_keys = ON")
        return g.db
    except RuntimeError:
        # Standalone context
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn


def close_db(e=None):
    """Close the database connection at the end of the request."""
    try:
        db = g.pop("db", None)
        if db is not None:
            db.close()
    except RuntimeError:
        pass


def init_db(db_path=None):
    """Initialize schema tables and indexes."""
    conn = get_db(db_path)
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    return conn
