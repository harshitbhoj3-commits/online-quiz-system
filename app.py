"""
QuizMaster — Online Quiz System
Main Application Factory and Entry Point
Course: BBAT104 — Fundamentals of Total Quality Management
Academic Session: 2026–27
Student Roll Number: 19
Core TQM Objective: Minimize latency during quiz submissions and ensure accurate automatic grading.
"""

from flask import Flask, render_template, redirect, url_for, session
from config import Config
from database import close_db, init_db
from services.auth_service import get_current_user
from routes.auth import auth_bp
from routes.student import student_bp
from routes.admin import admin_bp
from routes.quality import quality_bp


def create_app(test_config=None):
    """Application factory for QuizMaster."""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_object(test_config)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(quality_bp)

    # Database connection teardown
    app.teardown_appcontext(close_db)

    # Inject global context into all templates
    @app.context_processor
    def inject_global_template_vars():
        return {
            "app_title": Config.APP_TITLE,
            "course": Config.COURSE,
            "session_year": Config.ACADEMIC_SESSION,
            "roll_number": Config.STUDENT_ROLL_NUMBER,
            "quality_goal": Config.QUALITY_GOAL,
            "core_goal": Config.CORE_TQM_GOAL,
            "current_user": get_current_user(),
        }

    # Public Homepage
    @app.route("/")
    def index():
        if session.get("user_id"):
            if session.get("role") == "admin":
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("student.dashboard"))
        return render_template("index.html")

    # Error Handlers
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("errors/500.html"), 500

    return app


if __name__ == "__main__":
    app = create_app()
    print("=====================================================================")
    print("  QuizMaster — Online Quiz System")
    print(f"  Course: {Config.COURSE}")
    print(f"  Academic Session: {Config.ACADEMIC_SESSION} | Roll No: {Config.STUDENT_ROLL_NUMBER}")
    print("  Development Server starting at http://127.0.0.1:5000")
    print("=====================================================================")
    app.run(host="127.0.0.1", port=5000, debug=True)
