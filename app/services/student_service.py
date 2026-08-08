from Online_Quiz_Platform.app.models.quiz import Quiz
from Online_Quiz_Platform.app.extensions import db
from Online_Quiz_Platform.app.models.attempt import Attempt
from Online_Quiz_Platform.app.models.response import Response
from Online_Quiz_Platform.app.models.choice import Choice

def get_all_quizzes():
    """
    Returns all quizzes ordered by title.
    """

    quizzes = Quiz.query.order_by(Quiz.title).all()

    return quizzes

def create_attempt(user_id, quiz_id):
    """
    Create a new quiz attempt for a student.
    """

    attempt = Attempt(
        user_id=user_id,
        quiz_id=quiz_id
    )

    db.session.add(attempt)
    db.session.commit()

    return attempt


def save_response(attempt_id, question_id, choice_id):

    response = Response.query.filter_by(
        attempt_id=attempt_id,
        question_id=question_id
    ).first()

    if response:

        response.selected_choice_id = choice_id

    else:

        response = Response(
            attempt_id=attempt_id,
            question_id=question_id,
            selected_choice_id=choice_id
        )

        db.session.add(response)

    db.session.commit()



def calculate_score(attempt):

    score = 0
    total_marks = 0

    for response in attempt.responses:

        question = response.question
        total_marks += question.marks

        if response.selected_choice.is_correct:
            score += question.marks

    percentage = 0

    if total_marks > 0:
        percentage = (score / total_marks) * 100

    return score, percentage

def update_attempt_result(attempt):

    score, percentage = calculate_score(attempt)

    attempt.score = score
    attempt.percentage = percentage

    db.session.commit()