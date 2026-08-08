from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from Online_Quiz_Platform.app.services.student_service import (
    get_all_quizzes,
    create_attempt,
    save_response,
    update_attempt_result
)

from Online_Quiz_Platform.app.models.attempt import Attempt
from Online_Quiz_Platform.app.models.question import Question

student = Blueprint(
    "student",
    __name__,
    url_prefix="/student"
)


@student.route("/quizzes")
@login_required
def quizzes():

    # Prevent admins from using student pages
    if current_user.is_admin:
        return render_template("dashboard/admin_dashboard.html")

    quizzes = get_all_quizzes()

    return render_template(
        "student/quizzes.html",
        quizzes=quizzes
    )


@student.route("/quiz/<int:quiz_id>/start")
@login_required
def start_quiz(quiz_id):

    # Admins should not take quizzes
    if current_user.is_admin:
        flash("Admins cannot take quizzes.", "danger")
        return redirect(url_for("main.dashboard"))

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


@student.route(
    "/attempt/<int:attempt_id>/question/<int:question_number>",
    methods=["GET", "POST"]
)
@login_required
def show_question(attempt_id, question_number):

    if current_user.is_admin:
        flash("Admins cannot take quizzes.", "danger")
        return redirect(url_for("main.dashboard"))

    attempt = Attempt.query.get_or_404(attempt_id)

    questions = attempt.quiz.questions

    if question_number < 1 or question_number > len(questions):
        flash("Invalid question number.", "danger")
        return redirect(url_for("student.quizzes"))

    question = questions[question_number - 1]

    if request.method == "POST":

        choice_id = request.form.get("choice")

        save_response(
            attempt.id,
            question.id,
            choice_id
        )

        if question_number < len(questions):

            return redirect(
                url_for(
                    "student.show_question",
                    attempt_id=attempt.id,
                    question_number=question_number + 1
                )
            )

        return redirect(
            url_for(
                "student.submit_quiz",
                attempt_id=attempt.id
            )
        )

    return render_template(
        "student/question.html",
        attempt=attempt,
        question=question,
        question_number=question_number,
        total_questions=len(questions)
    )


@student.route("/attempt/<int:attempt_id>/submit")
@login_required
def submit_quiz(attempt_id):

    if current_user.is_admin:
        flash("Admins cannot take quizzes.", "danger")
        return redirect(url_for("main.dashboard"))

    attempt = Attempt.query.get_or_404(attempt_id)

    # Prevent students from viewing other students' attempts
    if attempt.user_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("student.quizzes"))

    update_attempt_result(attempt)

    return render_template(
        "student/result.html",
        attempt=attempt
    )