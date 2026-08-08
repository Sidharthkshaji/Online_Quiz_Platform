from app.models.user import User
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.category import Category
from app.models.attempt import Attempt


def get_admin_dashboard_data():

    return {
        "quiz_count": Quiz.query.count(),

        "question_count": Question.query.count(),

        "student_count": User.query.filter_by(
            role="student"
        ).count(),

        "category_count": Category.query.count(),

        "recent_quizzes": Quiz.query.order_by(
            Quiz.created_at.desc()
        ).limit(5).all()
    }


def get_student_dashboard_data(user_id):

    quizzes = Quiz.query.order_by(
        Quiz.created_at.desc()
    ).limit(6).all()

    attempts = Attempt.query.filter_by(
        user_id=user_id
    ).order_by(
        Attempt.submitted_at.desc()
    ).all()

    completed_attempts = [
        attempt
        for attempt in attempts
        if attempt.submitted_at is not None
    ]

    attempt_count = len(completed_attempts)

    average_percentage = 0

    if attempt_count > 0:

        average_percentage = sum(
            attempt.percentage
            for attempt in completed_attempts
        ) / attempt_count

    recent_attempts = completed_attempts[:5]

    active_attempt = Attempt.query.filter(
        Attempt.user_id == user_id,
        Attempt.submitted_at.is_(None),
        Attempt.started_at.isnot(None)
    ).order_by(
        Attempt.started_at.desc()
    ).first()

    return {
        "quiz_count": Quiz.query.count(),
        "attempt_count": attempt_count,
        "average_percentage": average_percentage,
        "available_quizzes": quizzes,
        "recent_attempts": recent_attempts,
        "active_attempt": active_attempt
    }