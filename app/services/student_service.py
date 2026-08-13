from app.extensions import db
from app.models.quiz import Quiz
from app.models.attempt import Attempt
from app.models.response import Response
from app.services.attempt_service import (
    calculate_score,
    update_attempt_result,
    create_attempt
)
from app.services.response_service import save_response


def get_all_quizzes():
    """
    Return all quizzes ordered by ID.
    """
    return Quiz.query.order_by(Quiz.id.asc()).all()