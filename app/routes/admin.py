from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from Online_Quiz_Platform.app.models.category import Category
from Online_Quiz_Platform.app.forms.category_form import CategoryForm
from Online_Quiz_Platform.app.services.category_service import (
    get_all_categories,
    create_category,
    update_category,
    delete_category
)

from Online_Quiz_Platform.app.forms.quiz_form import QuizForm
from Online_Quiz_Platform.app.forms.question_form import QuestionForm
from Online_Quiz_Platform.app.models.quiz import Quiz
from Online_Quiz_Platform.app.models.question import Question


from Online_Quiz_Platform.app.services.quiz_service import (
    get_all_quizzes,
    get_quiz_by_id,
    get_category_choices,
    create_quiz,
    update_quiz,
    delete_quiz
)

from Online_Quiz_Platform.app.services.question_service import (
    get_questions_by_quiz,
    get_question_by_id,
    create_question,
    update_question,
    delete_question
)

admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin.route("/categories")
@login_required
def categories():

    # Only admins can access this page
    if not current_user.is_admin:
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for("main.dashboard"))

    categories = get_all_categories()

    return render_template(
        "admin/categories.html",
        categories=categories
    )


@admin.route("/categories/create", methods=["GET", "POST"])
@login_required
def create_category_route():

    if not current_user.is_admin:
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for("main.dashboard"))

    form = CategoryForm()

    if form.validate_on_submit():

        success, message = create_category(
            form.name.data,
            form.description.data
        )

        flash(
            message,
            "success" if success else "danger"
        )

        if success:
            return redirect(url_for("admin.categories"))

    return render_template(
        "admin/create_category.html",
        form=form
    )

@admin.route("/categories/edit/<int:category_id>", methods=["GET", "POST"])
@login_required
def edit_category(category_id):

    if not current_user.is_admin:
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for("main.dashboard"))

    category = Category.query.get_or_404(category_id)

    form = CategoryForm(obj=category)

    if form.validate_on_submit():

        success, message = update_category(
            category,
            form.name.data,
            form.description.data
        )

        flash(message, "success" if success else "danger")

        if success:
            return redirect(url_for("admin.categories"))

    return render_template(
        "admin/edit_category.html",
        form=form,
        category=category
    )


@admin.route("/categories/delete/<int:category_id>", methods=["POST"])
@login_required
def delete_category_route(category_id):

    if not current_user.is_admin:
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for("main.dashboard"))

    category = Category.query.get_or_404(category_id)

    success, message = delete_category(category)

    flash(message, "success" if success else "danger")

    return redirect(url_for("admin.categories"))


@admin.route("/quizzes")
@login_required
def quizzes():

    if not current_user.is_admin:
        flash("You are not authorized.", "danger")
        return redirect(url_for("main.dashboard"))

    quizzes = get_all_quizzes()

    return render_template(
        "admin/quizzes.html",
        quizzes=quizzes
    )

@admin.route("/quizzes/create", methods=["GET", "POST"])
@login_required
def create_quiz_route():

    if not current_user.is_admin:
        flash("You are not authorized.", "danger")
        return redirect(url_for("main.dashboard"))

    form = QuizForm()

    # Populate Category dropdown
    form.category.choices = get_category_choices()

    if form.validate_on_submit():

        success, message = create_quiz(
            title=form.title.data,
            description=form.description.data,
            category_id=form.category.data,
            difficulty=form.difficulty.data,
            time_limit=form.time_limit.data,
            created_by=current_user.id
        )

        flash(message, "success" if success else "danger")

        if success:
            return redirect(url_for("admin.quizzes"))

    return render_template(
        "admin/create_quiz.html",
        form=form
    )


@admin.route("/quizzes/edit/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def edit_quiz(quiz_id):

    if not current_user.is_admin:
        flash("You are not authorized.", "danger")
        return redirect(url_for("main.dashboard"))

    quiz = get_quiz_by_id(quiz_id)

    form = QuizForm(obj=quiz)
    form.category.choices = get_category_choices()

    if form.validate_on_submit():

        success, message = update_quiz(
            quiz,
            form.title.data,
            form.description.data,
            form.category.data,
            form.difficulty.data,
            form.time_limit.data
        )

        flash(message, "success" if success else "danger")

        if success:
            return redirect(url_for("admin.quizzes"))

    return render_template(
        "admin/edit_quiz.html",
        form=form,
        quiz=quiz
    )


@admin.route("/quizzes/delete/<int:quiz_id>", methods=["POST"])
@login_required
def delete_quiz_route(quiz_id):

    if not current_user.is_admin:
        flash("You are not authorized.", "danger")
        return redirect(url_for("main.dashboard"))

    quiz = get_quiz_by_id(quiz_id)

    success, message = delete_quiz(quiz)

    flash(message, "success" if success else "danger")

    return redirect(url_for("admin.quizzes"))


@admin.route("/quizzes/<int:quiz_id>/questions")
@login_required
def questions(quiz_id):

    if not current_user.is_admin:
        flash("You are not authorized.", "danger")
        return redirect(url_for("main.dashboard"))

    quiz = Quiz.query.get_or_404(quiz_id)

    questions = get_questions_by_quiz(quiz_id)

    return render_template(
        "admin/questions.html",
        quiz=quiz,
        questions=questions
    )


@admin.route("/quizzes/<int:quiz_id>/questions/create", methods=["GET", "POST"])
@login_required
def create_question_route(quiz_id):

    if not current_user.is_admin:
        flash("You are not authorized.", "danger")
        return redirect(url_for("main.dashboard"))

    quiz = Quiz.query.get_or_404(quiz_id)

    form = QuestionForm()

    if form.validate_on_submit():

        success, message = create_question(
            quiz_id=quiz.id,
            question_text=form.question_text.data,
            marks=form.marks.data,
            choice_a=form.choice_a.data,
            choice_b=form.choice_b.data,
            choice_c=form.choice_c.data,
            choice_d=form.choice_d.data,
            correct_choice=form.correct_choice.data
        )

        flash(message, "success" if success else "danger")

        if success:
            return redirect(
                url_for(
                    "admin.questions",
                    quiz_id=quiz.id
                )
            )

    return render_template(
        "admin/create_question.html",
        form=form,
        quiz=quiz
    )



@admin.route("/questions/edit/<int:question_id>", methods=["GET", "POST"])
@login_required
def edit_question(question_id):

    if not current_user.is_admin:
        flash("You are not authorized.", "danger")
        return redirect(url_for("main.dashboard"))

    question = get_question_by_id(question_id)

    form = QuestionForm()

    # -----------------------
    # Pre-fill the form (GET)
    # -----------------------
    if not form.is_submitted():

        form.question_text.data = question.question_text
        form.marks.data = question.marks

        form.choice_a.data = question.choices[0].choice_text
        form.choice_b.data = question.choices[1].choice_text
        form.choice_c.data = question.choices[2].choice_text
        form.choice_d.data = question.choices[3].choice_text

        if question.choices[0].is_correct:
            form.correct_choice.data = "A"
        elif question.choices[1].is_correct:
            form.correct_choice.data = "B"
        elif question.choices[2].is_correct:
            form.correct_choice.data = "C"
        else:
            form.correct_choice.data = "D"

    # -----------------------
    # Save changes (POST)
    # -----------------------
    if form.validate_on_submit():

        success, message = update_question(
            question,
            form.question_text.data,
            form.marks.data,
            form.choice_a.data,
            form.choice_b.data,
            form.choice_c.data,
            form.choice_d.data,
            form.correct_choice.data
        )

        flash(message, "success" if success else "danger")

        if success:
            return redirect(
                url_for(
                    "admin.questions",
                    quiz_id=question.quiz_id
                )
            )

    return render_template(
        "admin/edit_question.html",
        form=form,
        question=question
    )



@admin.route("/questions/delete/<int:question_id>", methods=["POST"])
@login_required
def delete_question_route(question_id):

    if not current_user.is_admin:
        flash("You are not authorized.", "danger")
        return redirect(url_for("main.dashboard"))

    question = get_question_by_id(question_id)

    quiz_id = question.quiz.id

    success, message = delete_question(question)

    flash(message, "success" if success else "danger")

    return redirect(
        url_for(
            "admin.questions",
            quiz_id=quiz_id
        )
    )