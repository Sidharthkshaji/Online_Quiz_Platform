from datetime import datetime, timedelta

from app.extensions import db
from app.models.attempt import Attempt


def create_attempt(user_id, quiz_id):
    """
    Create a new attempt for a student.
    """

    attempt = Attempt(
        user_id=user_id,
        quiz_id=quiz_id,
        started_at=datetime.utcnow()
    )

    db.session.add(attempt)
    db.session.commit()

    return attempt


def get_attempt_by_id(attempt_id):
    """
    Return an attempt by ID.
    """

    return Attempt.query.get_or_404(attempt_id)


def get_student_attempt(attempt_id, user_id):
    """
    Return an attempt only if it belongs to the student.
    """

    attempt = Attempt.query.get_or_404(attempt_id)

    if attempt.user_id != user_id:
        return None

    return attempt


def get_active_attempt(user_id):
    """
    Return the student's unfinished attempt.
    """

    return Attempt.query.filter(
        Attempt.user_id == user_id,
        Attempt.submitted_at.is_(None),
        Attempt.started_at.isnot(None)
    ).order_by(
        Attempt.started_at.desc()
    ).first()


def calculate_score(attempt):
    """
    Calculate score and percentage.
    Total marks is based on ALL questions in the quiz, not just answered ones.
    """

    score = 0
    total_marks = sum(q.marks for q in attempt.quiz.questions)

    for response in attempt.responses:
        if response.selected_choice and response.selected_choice.is_correct:
            score += response.question.marks

    percentage = 0

    if total_marks > 0:
        percentage = (score / total_marks) * 100

    return score, percentage


def update_attempt_result(attempt):
    """
    Calculate and save the final quiz result.
    """

    score, percentage = calculate_score(attempt)

    attempt.score = score
    attempt.percentage = percentage

    attempt.submitted_at = datetime.utcnow()

    if attempt.started_at:
        attempt.time_taken = int(
            (
                attempt.submitted_at -
                attempt.started_at
            ).total_seconds()
        )

    db.session.commit()

    return attempt


def get_attempt_deadline(attempt):
    """
    Return the exact time when the quiz expires.
    """

    if not attempt.started_at:
        return None

    return attempt.started_at + timedelta(
        minutes=attempt.quiz.time_limit
    )


def is_attempt_expired(attempt):
    """
    Check whether the attempt has exceeded
    the quiz time limit.
    """

    if attempt.submitted_at is not None:
        return False

    deadline = get_attempt_deadline(attempt)

    if deadline is None:
        return False

    return datetime.utcnow() >= deadline


def expire_attempt(attempt):
    """
    Automatically submit an expired attempt.
    """

    if attempt.submitted_at is not None:
        return attempt

    score, percentage = calculate_score(attempt)

    attempt.score = score
    attempt.percentage = percentage

    attempt.submitted_at = datetime.utcnow()

    if attempt.started_at:
        attempt.time_taken = int(
            (
                attempt.submitted_at -
                attempt.started_at
            ).total_seconds()
        )

    db.session.commit()

    return attempt