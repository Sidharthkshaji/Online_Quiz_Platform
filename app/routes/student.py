from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import login_required, current_user

from app.services.student_service import (
    get_all_quizzes
)

from app.services.attempt_service import (
    create_attempt,
    update_attempt_result,
    get_attempt_by_id,
    is_attempt_expired,
    expire_attempt,
    get_attempt_deadline
)

from app.services.response_service import (
    save_response,
    get_response_for_question
)


student = Blueprint(
    "student",
    __name__,
    url_prefix="/student"
)


# --------------------------------------------------
# AVAILABLE QUIZZES
# --------------------------------------------------

@student.route("/quizzes")
@login_required
def quizzes():

    if current_user.is_admin:

        return redirect(
            url_for("admin.quizzes")
        )

    quizzes = get_all_quizzes()

    return render_template(
        "student/quizzes.html",
        quizzes=quizzes
    )


# --------------------------------------------------
# START QUIZ
# --------------------------------------------------

@student.route("/quiz/<int:quiz_id>/start")
@login_required
def start_quiz(quiz_id):

    if current_user.is_admin:

        flash(
            "Admins cannot take quizzes.",
            "danger"
        )

        return redirect(
            url_for("main.dashboard")
        )

    attempt = create_attempt(
        current_user.id,
        quiz_id
    )

    return redirect(
        url_for(
            "student.show_question",
            attempt_id=attempt.id,
            question_number=1
        )
    )


# --------------------------------------------------
# SHOW QUESTION
# --------------------------------------------------

@student.route(
    "/attempt/<int:attempt_id>/question/<int:question_number>",
    methods=["GET", "POST"]
)
@login_required
def show_question(
    attempt_id,
    question_number
):

    if current_user.is_admin:

        flash(
            "Admins cannot take quizzes.",
            "danger"
        )

        return redirect(
            url_for("main.dashboard")
        )

    attempt = get_attempt_by_id(attempt_id)

    # Security check
    if attempt.user_id != current_user.id:

        flash(
            "Unauthorized access.",
            "danger"
        )

        return redirect(
            url_for("student.quizzes")
        )

    # Already completed
    if attempt.submitted_at is not None:

        return redirect(
            url_for(
                "student.submit_quiz",
                attempt_id=attempt.id
            )
        )

    # --------------------------------------------------
    # SERVER-SIDE TIME CHECK
    # --------------------------------------------------

    if is_attempt_expired(attempt):

        expire_attempt(attempt)

        flash(
            "Time is up. Your quiz has been submitted automatically.",
            "warning"
        )

        return redirect(
            url_for(
                "student.submit_quiz",
                attempt_id=attempt.id
            )
        )

    questions = attempt.quiz.questions

    if not questions:

        flash(
            "This quiz has no questions.",
            "danger"
        )

        return redirect(
            url_for("student.quizzes")
        )

    if (
        question_number < 1
        or question_number > len(questions)
    ):

        flash(
            "Invalid question number.",
            "danger"
        )

        return redirect(
            url_for("student.quizzes")
        )

    question = questions[
        question_number - 1
    ]

    # --------------------------------------------------
    # POST
    # --------------------------------------------------

    if request.method == "POST":

        action = request.form.get("action")

        choice_id = request.form.get("choice")

        # Save selected answer
        if choice_id:

            save_response(
                attempt.id,
                question.id,
                int(choice_id)
            )

        # ------------------------------------------
        # Timer expired
        # ------------------------------------------

        if action == "time_expired":

            expire_attempt(attempt)

            return redirect(
                url_for(
                    "student.submit_quiz",
                    attempt_id=attempt.id
                )
            )

        # ------------------------------------------
        # Check server time again
        # ------------------------------------------

        if is_attempt_expired(attempt):

            expire_attempt(attempt)

            flash(
                "Time is up. Your quiz has been submitted automatically.",
                "warning"
            )

            return redirect(
                url_for(
                    "student.submit_quiz",
                    attempt_id=attempt.id
                )
            )

        # ------------------------------------------
        # Previous
        # ------------------------------------------

        if action == "previous":

            return redirect(
                url_for(
                    "student.show_question",
                    attempt_id=attempt.id,
                    question_number=question_number - 1
                )
            )

        # ------------------------------------------
        # Next
        # ------------------------------------------

        if action == "next":

            return redirect(
                url_for(
                    "student.show_question",
                    attempt_id=attempt.id,
                    question_number=question_number + 1
                )
            )

        # ------------------------------------------
        # Submit
        # ------------------------------------------

        if action == "submit":

            return redirect(
                url_for(
                    "student.submit_quiz",
                    attempt_id=attempt.id
                )
            )

    # --------------------------------------------------
    # GET
    # --------------------------------------------------

    previous_response = get_response_for_question(
        attempt.id,
        question.id
    )

    selected_choice_id = None

    if previous_response:

        selected_choice_id = (
            previous_response.selected_choice_id
        )

    # Calculate remaining time
    deadline = get_attempt_deadline(attempt)

    remaining_seconds = 0

    if deadline:

        remaining_seconds = max(
            0,
            int(
                (
                    deadline -
                    datetime.utcnow()
                ).total_seconds()
            )
        )

    return render_template(
        "student/question.html",
        attempt=attempt,
        question=question,
        question_number=question_number,
        total_questions=len(questions),
        selected_choice_id=selected_choice_id,
        quiz_active=True,
        remaining_seconds=remaining_seconds
    )


# --------------------------------------------------
# SUBMIT QUIZ
# --------------------------------------------------

@student.route(
    "/attempt/<int:attempt_id>/submit"
)
@login_required
def submit_quiz(attempt_id):

    if current_user.is_admin:

        flash(
            "Admins cannot review quiz attempts.",
            "danger"
        )

        return redirect(
            url_for("main.dashboard")
        )

    attempt = get_attempt_by_id(attempt_id)

    if attempt.user_id != current_user.id:

        flash(
            "Unauthorized access.",
            "danger"
        )

        return redirect(
            url_for("student.quizzes")
        )

    # Only calculate final result if not already submitted
    if attempt.submitted_at is None:

        update_attempt_result(attempt)

    return render_template(
        "student/result.html",
        attempt=attempt
    )


# --------------------------------------------------
# REVIEW ANSWERS
# --------------------------------------------------

@student.route(
    "/attempt/<int:attempt_id>/review"
)
@login_required
def review_attempt(attempt_id):

    if current_user.is_admin:

        flash(
            "Admins cannot review quiz attempts.",
            "danger"
        )

        return redirect(
            url_for("main.dashboard")
        )

    attempt = get_attempt_by_id(attempt_id)

    if attempt.user_id != current_user.id:

        flash(
            "Unauthorized access.",
            "danger"
        )

        return redirect(
            url_for("student.quizzes")
        )

    return render_template(
        "student/review.html",
        attempt=attempt
    )