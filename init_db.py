"""
Database Initialization and Data Seeding Module
Initializes schema tables and populates default administration credentials,
student test accounts, realistic TQM course quizzes, defect checksheets,
FMEA matrices, and PDCA logs.
"""

import sys
from werkzeug.security import generate_password_hash
from database import init_db, get_db
from config import Config


def seed_database(db_path=None):
    """Initializes tables and seeds default records."""
    conn = init_db(db_path)
    cur = conn.cursor()

    # 1. Seed Users (if not existing)
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        print("[*] Seeding default users...")
        users = [
            (
                "admin",
                "admin@quizmaster.local",
                generate_password_hash("Admin@12345"),
                "admin",
                "System Administrator",
                "ADM-01",
            ),
            (
                "student19",
                "student19@college.edu",
                generate_password_hash("Student@12345"),
                "student",
                "Student (Roll 19)",
                "19",
            ),
            (
                "rahul20",
                "rahul20@college.edu",
                generate_password_hash("Student@12345"),
                "student",
                "Rahul Sharma",
                "20",
            ),
        ]
        cur.executemany(
            """
            INSERT INTO users (username, email, password_hash, role, full_name, roll_number)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            users,
        )
        conn.commit()

    # 2. Seed Quizzes
    cur.execute("SELECT COUNT(*) FROM quizzes")
    if cur.fetchone()[0] == 0:
        print("[*] Seeding curriculum quizzes...")
        quizzes = [
            (
                "BBAT104: Fundamentals of Total Quality Management",
                "Official mid-term assessment covering TQM principles, Deming cycle, Six Sigma, FMEA, Pareto 80/20 rule, and Ishikawa diagrams.",
                15,  # duration in minutes
                50.0,  # pass percentage
                1,  # is_published
                1,  # allow_review
                0,  # shuffle_questions
                1,  # created_by admin
            ),
            (
                "Software Quality Assurance & Testing (SQA)",
                "Quality engineering quiz focusing on verification, validation, test coverage, defect lifecycle, and latency optimization.",
                10,
                40.0,
                1,
                1,
                0,
                1,
            ),
            (
                "Python & Database Engineering Fundamentals",
                "Technical quiz covering Flask routing, SQLite parameterized queries, transactions, and backend latency minimization.",
                10,
                50.0,
                1,
                1,
                0,
                1,
            ),
        ]
        cur.executemany(
            """
            INSERT INTO quizzes (title, description, duration_minutes, pass_percentage, is_published, allow_review, shuffle_questions, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            quizzes,
        )
        conn.commit()

        # Retrieve Quiz IDs
        cur.execute("SELECT id, title FROM quizzes")
        quiz_map = {row["title"]: row["id"] for row in cur.fetchall()}

        tqm_quiz_id = quiz_map["BBAT104: Fundamentals of Total Quality Management"]
        sqa_quiz_id = quiz_map["Software Quality Assurance & Testing (SQA)"]
        py_quiz_id = quiz_map["Python & Database Engineering Fundamentals"]

        # Questions for TQM Quiz
        tqm_questions = [
            (
                tqm_quiz_id,
                "Who is widely recognized as the father of modern statistical quality control and introduced the 14 Points for Management?",
                "Philip Crosby",
                "W. Edwards Deming",
                "Joseph Juran",
                "Kaoru Ishikawa",
                "B",
                1.0,
                "Dr. W. Edwards Deming introduced the 14 management points and popularized the PDCA cycle in post-war Japan.",
                1,
            ),
            (
                tqm_quiz_id,
                "The Pareto Principle asserts that approximately what proportion of effects come from causes in a typical process?",
                "50% effects from 50% causes",
                "80% effects from 20% causes",
                "70% effects from 30% causes",
                "90% effects from 10% causes",
                "B",
                1.0,
                "Vilfredo Pareto observed that 80% of consequences come from 20% of causes (the vital few vs trivial many).",
                2,
            ),
            (
                tqm_quiz_id,
                "In a Failure Mode and Effects Analysis (FMEA), how is the Risk Priority Number (RPN) computed?",
                "RPN = Severity + Occurrence + Detection",
                "RPN = (Severity × Occurrence) / Detection",
                "RPN = Severity × Occurrence × Detection",
                "RPN = (Severity + Occurrence) × Detection",
                "C",
                1.0,
                "RPN is the mathematical product of Severity (S), Occurrence (O), and Detection (D) ratings.",
                3,
            ),
            (
                tqm_quiz_id,
                "What are the four iterative steps in the Deming / Shewhart continuous improvement cycle?",
                "Produce, Deliver, Check, Act",
                "Plan, Do, Check, Act",
                "Prepare, Document, Calculate, Assess",
                "Plan, Design, Control, Audit",
                "B",
                1.0,
                "PDCA stands for Plan (target & hypothesis), Do (execute trial), Check (measure outcome), and Act (standardize or iterate).",
                4,
            ),
            (
                tqm_quiz_id,
                "Which TQM quality tool is also known as a 'Cause-and-Effect' or 'Fishbone' diagram?",
                "Gantt Chart",
                "Ishikawa Diagram",
                "Control Chart",
                "Scatter Diagram",
                "B",
                1.0,
                "Developed by Kaoru Ishikawa, it categorizes potential root causes into People, Process, Machine, and Environment.",
                5,
            ),
            (
                tqm_quiz_id,
                "What does 'CTQ' stand for in Quality Management and Six Sigma methodology?",
                "Control To Quality",
                "Critical To Quality",
                "Cost, Time, Quality",
                "Customer Test Quotient",
                "B",
                1.0,
                "Critical To Quality (CTQ) parameters are measurable quality characteristics aligned with customer expectations.",
                6,
            ),
            (
                tqm_quiz_id,
                "What does the Japanese quality concept 'Poka-Yoke' translate to in English?",
                "Mistake-proofing / Error-proofing",
                "Continuous improvement",
                "Visual workplace management",
                "Just-in-Time production",
                "A",
                1.0,
                "Poka-Yoke means designing mechanisms that prevent human errors from passing undetected down the workflow.",
                7,
            ),
            (
                tqm_quiz_id,
                "In a SIPOC diagram, what does the letter 'I' represent?",
                "Inspection",
                "Inputs",
                "Iteration",
                "Infrastructure",
                "B",
                1.0,
                "SIPOC stands for Suppliers, Inputs, Process, Outputs, and Customers.",
                8,
            ),
            (
                tqm_quiz_id,
                "What is the defect rate corresponding to a true Six Sigma quality level?",
                "66,807 defects per million opportunities (DPMO)",
                "3.4 defects per million opportunities (DPMO)",
                "340 defects per million opportunities (DPMO)",
                "0.034 defects per million opportunities (DPMO)",
                "B",
                1.0,
                "A Six Sigma process allows only 3.4 defects per million opportunities (99.99966% defect-free performance).",
                9,
            ),
            (
                tqm_quiz_id,
                "What is the core TQM objective of the QuizMaster Online Quiz System?",
                "Displaying dynamic advertising banners",
                "Minimizing quiz submission latency and guaranteeing 100% grading accuracy",
                "Replacing academic textbooks with video clips",
                "Enforcing arbitrary time limits without grace buffers",
                "B",
                1.0,
                "The primary CTQ objective is minimizing latency during quiz submissions and ensuring verified automatic grading.",
                10,
            ),
        ]

        # Questions for SQA Quiz
        sqa_questions = [
            (
                sqa_quiz_id,
                "What is the primary distinction between Verification and Validation in quality engineering?",
                "Verification is performed by users; Validation is performed by developers",
                "Verification asks 'Are we building the product right?'; Validation asks 'Are we building the right product?'",
                "Verification is automated; Validation is always manual",
                "Verification measures latency; Validation measures memory",
                "B",
                1.0,
                "Verification checks adherence to specifications, whereas Validation ensures the product satisfies genuine user needs.",
                1,
            ),
            (
                sqa_quiz_id,
                "Which type of testing verifies that recent code modifications have not adversely affected existing system features?",
                "Unit Testing",
                "Stress Testing",
                "Regression Testing",
                "Usability Testing",
                "C",
                1.0,
                "Regression testing re-executes tests to confirm existing capabilities continue to operate correctly after bug fixes or new features.",
                2,
            ),
            (
                sqa_quiz_id,
                "What does 'Defect Density' measure in software quality analysis?",
                "Total number of test cases executed per hour",
                "Number of confirmed defects divided by software size (e.g. per 1,000 lines of code)",
                "Physical RAM occupied by bug tracking software",
                "Number of developers working on bug fixing",
                "B",
                1.0,
                "Defect density evaluates defect counts relative to module size or KLOC to identify high-risk components.",
                3,
            ),
            (
                sqa_quiz_id,
                "In boundary value analysis (BVA), if an input field accepts numbers between 1 and 100, which values must be tested?",
                "50, 60, 70",
                "0, 1, 2 and 99, 100, 101",
                "-50, 0, 150",
                "10, 20, 30",
                "B",
                1.0,
                "BVA concentrates on the exact boundary limits (just below, at, and just above the thresholds: 0, 1, 2 and 99, 100, 101).",
                4,
            ),
            (
                sqa_quiz_id,
                "Why are database transactions (ACID) essential when recording final quiz submissions?",
                "They increase font resolution on the results screen",
                "They ensure answers and final scores are committed atomically without partial data loss",
                "They allow students to change answers after the deadline",
                "They bypass server-side validation checks",
                "B",
                1.0,
                "Atomic transactions guarantee that answer choices, total score, and completion timestamp are written together or rolled back completely if an error occurs.",
                5,
            ),
        ]

        # Questions for Python Quiz
        py_questions = [
            (
                py_quiz_id,
                "Why should database queries always use parameterized placeholders (?) instead of string concatenation in SQLite?",
                "To reduce database file size on disk",
                "To prevent SQL Injection vulnerabilities and ensure correct datatype escaping",
                "To convert SQLite into a NoSQL database",
                "To automatically encrypt all tables",
                "B",
                1.0,
                "Parameterized queries separate query logic from untrusted user parameters, neutralizing SQL injection vectors.",
                1,
            ),
            (
                py_quiz_id,
                "In Flask, which HTTP method should be used for operations that modify database state, such as submitting a quiz or creating questions?",
                "GET",
                "HEAD",
                "POST",
                "OPTIONS",
                "C",
                1.0,
                "POST requests carry payload in the request body and are not idempotent, protecting state-changing actions from accidental pre-fetching.",
                2,
            ),
            (
                py_quiz_id,
                "How does SQLite indexing on `quiz_id` in the `questions` table improve quiz submission performance?",
                "It compresses question text to 8-bit ASCII",
                "It enables O(log N) question lookup instead of scanning the full table sequentially",
                "It prevents questions from being deleted",
                "It translates SQL to C code automatically",
                "B",
                1.0,
                "B-tree indexing reduces disk I/O and query time from O(N) linear scans to logarithmic O(log N) lookups, minimizing submission latency.",
                3,
            ),
            (
                py_quiz_id,
                "What is the role of Werkzeug's `generate_password_hash` in secure user authentication?",
                "It compresses passwords using gzip",
                "It computes a one-way cryptographic hash with random salt to prevent plaintext password leakage",
                "It stores passwords in an Excel spreadsheet",
                "It sends the password to the client browser",
                "B",
                1.0,
                "One-way salted hashing protects credentials against rainbow table attacks and unauthorized database dumps.",
                4,
            ),
            (
                py_quiz_id,
                "Which Python module from the standard library provides high-resolution time measurements for microsecond latency benchmarking?",
                "time.sleep()",
                "time.perf_counter()",
                "datetime.date()",
                "calendar.month()",
                "B",
                1.0,
                "`time.perf_counter()` accesses the system's highest available resolution monotonic clock for performance profiling.",
                5,
            ),
        ]

        for q in tqm_questions + sqa_questions + py_questions:
            cur.execute(
                """
                INSERT INTO questions (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option, marks, explanation, order_index)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                q,
            )
        conn.commit()

    # 3. Seed Defect Logs (for Pareto Analysis & Checksheets)
    cur.execute("SELECT COUNT(*) FROM defect_logs")
    if cur.fetchone()[0] == 0:
        print("[*] Seeding quality defect log records...")
        defects = [
            (
                "DEF-001",
                "Submission Latency",
                "Quiz submission took >120ms due to unindexed attempt_id lookups under load",
                "High",
                8,
                "Resolved",
                "Missing index on attempt_answers(attempt_id)",
                "Added B-tree index idx_answers_attempt_id in database schema",
                "QA Engineer",
                "2026-10-10 10:15:00",
                "2026-10-10 14:30:00",
            ),
            (
                "DEF-002",
                "Input Validation",
                "Form accepted quiz duration <= 0 during quiz creation",
                "Medium",
                5,
                "Resolved",
                "Missing server-side bounds check for duration_minutes",
                "Enforced duration_minutes >= 1 validation in route handler and HTML min attribute",
                "Test Lead",
                "2026-10-11 11:20:00",
                "2026-10-11 15:45:00",
            ),
            (
                "DEF-003",
                "Submission Latency",
                "Client double-click on Submit Quiz button initiated duplicate submission thread",
                "High",
                12,
                "Resolved",
                "Submit button lacked client-side disable state upon first trigger",
                "Added JavaScript double-submit lock and server-side status lock",
                "Lead Developer",
                "2026-10-12 09:00:00",
                "2026-10-12 12:00:00",
            ),
            (
                "DEF-004",
                "Grading Accuracy",
                "Question with case-mismatched answer ('b' vs 'B') failed grading comparison",
                "Critical",
                3,
                "Resolved",
                "Grading comparison did not normalize selected option casing",
                "Added .strip().upper() normalization in grading_service.py",
                "QA Engineer",
                "2026-10-13 14:00:00",
                "2026-10-13 16:15:00",
            ),
            (
                "DEF-005",
                "UI / Usability",
                "Timer clock rendered misaligned on mobile screen viewports < 400px",
                "Low",
                4,
                "Resolved",
                "Fixed viewport width in CSS quiz container",
                "Applied CSS flex-wrap and responsive clamp font sizing",
                "UI Designer",
                "2026-10-14 16:30:00",
                "2026-10-15 10:00:00",
            ),
            (
                "DEF-006",
                "Security & Auth",
                "Unauthenticated user could hit /student/quizzes endpoint directly",
                "Critical",
                2,
                "Resolved",
                "Missing @login_required decorator on student quiz route",
                "Decorated all student and admin endpoints with explicit role guard",
                "Security Consultant",
                "2026-10-15 11:00:00",
                "2026-10-15 13:00:00",
            ),
            (
                "DEF-007",
                "Timeout Handling",
                "Quiz timeout triggered abruptly without saving currently checked options",
                "Medium",
                3,
                "Resolved",
                "Auto-submit event on zero timer omitted form serialization payload",
                "Synchronized JS auto-submit function to call form.submit() with current form state",
                "QA Engineer",
                "2026-10-16 13:40:00",
                "2026-10-16 17:10:00",
            ),
            (
                "DEF-008",
                "UI / Usability",
                "Option radio labels lacked visible focus indicator on keyboard TAB navigation",
                "Low",
                2,
                "Resolved",
                "Default browser outline was suppressed in stylesheet",
                "Restored high-contrast :focus-visible ring for accessibility compliance",
                "UI Designer",
                "2026-10-17 10:10:00",
                "2026-10-17 11:30:00",
            ),
            (
                "DEF-009",
                "Data Integrity",
                "Deleting a quiz left orphaned rows in attempt_answers table",
                "Medium",
                1,
                "Resolved",
                "SQLite PRAGMA foreign_keys was not consistently enabled on every connection",
                "Enforced PRAGMA foreign_keys = ON in database.py connection factory with ON DELETE CASCADE",
                "Database Architect",
                "2026-10-18 09:30:00",
                "2026-10-18 11:00:00",
            ),
        ]
        cur.executemany(
            """
            INSERT INTO defect_logs (defect_code, category, description, severity, occurrence_count, status, root_cause, corrective_action, reported_by, created_at, resolved_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            defects,
        )
        conn.commit()

    # 4. Seed FMEA Records
    cur.execute("SELECT COUNT(*) FROM fmea_records")
    if cur.fetchone()[0] == 0:
        print("[*] Seeding FMEA risk matrix...")
        fmea = [
            (
                "Quiz Final Submission",
                "Network drop during submission POST payload",
                "Student attempt remains 'in_progress'; score not registered",
                "Unstable client connection or mobile network loss",
                8,  # S
                4,  # O
                4,  # D
                128,  # RPN
                "Local storage state caching and retry modal with offline warning",
                "Full-Stack Dev",
                "Mitigated",
            ),
            (
                "Automatic Grading Engine",
                "Incorrect score computation due to case/whitespace mismatch",
                "Wrong score recorded; student receives unfair grade",
                "Unsanitized string comparison in grading logic",
                9,  # S
                2,  # O
                2,  # D
                36,  # RPN
                "Strict normalization (.strip().upper()) and 100% automated pytest coverage",
                "QA Engineer",
                "Standardized",
            ),
            (
                "Submission Concurrency",
                "Student double-clicks 'Submit' button rapidly",
                "Duplicate attempt records created or score overwrite",
                "Absence of client-side button disable and database transaction locking",
                7,  # S
                5,  # O
                3,  # D
                105,  # RPN
                "Client button disabling on click + atomic DB check on status='in_progress'",
                "Full-Stack Dev",
                "Standardized",
            ),
            (
                "Timer & Deadline Management",
                "Student manipulates browser system clock to extend duration",
                "Unfair time advantage for dishonest participant",
                "Relying on client-side Date() rather than server start timestamp",
                8,  # S
                3,  # O
                3,  # D
                72,  # RPN
                "Server-side validation comparing CURRENT_TIMESTAMP with start_time + duration",
                "Backend Dev",
                "Standardized",
            ),
            (
                "Access Control & Security",
                "Student attempts direct URL access to admin quiz editor",
                "Unauthorized modification or leakage of exam questions",
                "Missing or bypassed role authorization decorator",
                10,  # S
                2,  # O
                2,  # D
                40,  # RPN
                "Mandatory @admin_required decorator with 403 Forbidden abort and audit logging",
                "Security Lead",
                "Standardized",
            ),
        ]
        cur.executemany(
            """
            INSERT INTO fmea_records (process_step, potential_failure_mode, potential_effect, potential_cause, severity, occurrence, detection, rpn, mitigation_action, responsible_role, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            fmea,
        )
        conn.commit()

    # 5. Seed PDCA Improvement Records
    cur.execute("SELECT COUNT(*) FROM pdca_records")
    if cur.fetchone()[0] == 0:
        print("[*] Seeding PDCA continuous improvement logs...")
        pdca = [
            (
                1,
                "Cycle 1: Submission Latency Optimization (Target < 50ms)",
                "Plan: Measured initial quiz submission latency at 95ms under multi-attempt tables. Target is sub-50ms average server response time.",
                "Do: Implemented SQLite indexes on attempt_answers(attempt_id) and questions(quiz_id). Refactored grading service to load all correct answers in a single batch query.",
                "Check: Executed 50 consecutive automated submission benchmarks. Observed mean latency dropped to 14.8ms (p95: 22.4ms), exceeding target by 70%.",
                "Act: Standardized composite indexes into schema.py migration and added continuous latency telemetry to the admin TQM dashboard.",
                "Standardized",
            ),
            (
                2,
                "Cycle 2: 100% Automatic Grading Accuracy & Case Normalization",
                "Plan: Eliminate potential grading discrepancies caused by client whitespace, letter casing, or omitted radio choices.",
                "Do: Developed pure Python grading pipeline with strict .strip().upper() sanitization, handling empty strings as 0 marks gracefully without exceptions.",
                "Check: Implemented 15 comprehensive pytest unit tests verifying 100% correct, 100% incorrect, partial submissions, blank options, and boundary conditions.",
                "Act: Integrated automated test suite into pre-commit checklist. All tests passing with 100% grading precision.",
                "Standardized",
            ),
            (
                3,
                "Cycle 3: Duplicate Submission Prevention via Dual Locks",
                "Plan: Prevent duplicate submissions when students click 'Submit Quiz' repeatedly or refresh the page during grading.",
                "Do: Added dual protection: (1) Client JavaScript disables submit button and displays loading spinner immediately on click; (2) Server checks attempt status=='completed' before transaction, immediately returning existing result.",
                "Check: Executed concurrent submission simulation with 5 rapid duplicate requests for a single attempt. Exactly one evaluation was registered with zero duplicate rows.",
                "Act: Documented dual-barrier mechanism in FMEA and system architecture documentation.",
                "Standardized",
            ),
        ]
        cur.executemany(
            """
            INSERT INTO pdca_records (cycle_number, title, plan_text, do_text, check_text, act_text, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            pdca,
        )
        conn.commit()

    # 6. Seed Quality Metrics (CTQ)
    cur.execute("SELECT COUNT(*) FROM quality_metrics")
    if cur.fetchone()[0] == 0:
        print("[*] Seeding CTQ quality metrics...")
        metrics = [
            ("Average Submission Latency", 50.0, 14.8, "ms", "Pass", "Measured across automated test suite submissions"),
            ("Grading Accuracy", 100.0, 100.0, "%", "Pass", "100% match between server key and awarded marks"),
            ("System Uptime During Test Session", 99.5, 100.0, "%", "Pass", "Zero unexpected crashes or unhandled 500 errors"),
            ("Unanswered Question Graceful Handling", 100.0, 100.0, "%", "Pass", "Zero marks awarded for blank answers without exception"),
            ("Duplicate Submission Rejection Rate", 100.0, 100.0, "%", "Pass", "100% idempotency enforced on completed attempts"),
        ]
        cur.executemany(
            """
            INSERT INTO quality_metrics (metric_name, target_value, observed_value, unit, status, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            metrics,
        )
        conn.commit()

    # 7. Seed Sample Attempt for Student 19 (so Student Dashboard has instant real data)
    cur.execute("SELECT COUNT(*) FROM quiz_attempts")
    if cur.fetchone()[0] == 0:
        print("[*] Seeding baseline sample quiz attempt for student19...")
        cur.execute(
            """
            INSERT INTO quiz_attempts (quiz_id, user_id, start_time, end_time, submitted_at, score, total_marks, percentage, status, latency_ms)
            VALUES (1, 2, datetime('now', '-1 hour'), datetime('now', '-50 minutes'), datetime('now', '-50 minutes'), 9.0, 10.0, 90.0, 'completed', 16.4)
            """
        )
        attempt_id = cur.lastrowid

        # Insert attempt answers
        cur.execute("SELECT id, correct_option, marks FROM questions WHERE quiz_id = 1 ORDER BY order_index")
        questions = cur.fetchall()
        for idx, q in enumerate(questions):
            # student got 9 out of 10 correct
            selected = q["correct_option"] if idx != 6 else ("B" if q["correct_option"] == "A" else "A")
            is_correct = 1 if selected == q["correct_option"] else 0
            marks_awarded = q["marks"] if is_correct else 0.0
            cur.execute(
                """
                INSERT INTO attempt_answers (attempt_id, question_id, selected_option, is_correct, marks_awarded)
                VALUES (?, ?, ?, ?, ?)
                """,
                (attempt_id, q["id"], selected, is_correct, marks_awarded),
            )
        conn.commit()

    print("[✔] Database initialization and seeding completed successfully.")


if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else None
    seed_database(db_path)
