from app.extensions import db
from app.models.response import Response


def save_response(attempt_id, question_id, choice_id):
    """
    Save or update a student's answer.

    If the student comes back to the question and changes
    the answer, the existing response is updated.
    """

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

    return response


def get_response_for_question(attempt_id, question_id):
    """Return the student's response for a particular question."""

    return Response.query.filter_by(
        attempt_id=attempt_id,
        question_id=question_id
    ).first()


def get_attempt_responses(attempt_id):
    """Return all responses for an attempt."""

    return Response.query.filter_by(
        attempt_id=attempt_id
    ).all()

def get_answered_question_ids(attempt_id):

    responses = Response.query.filter_by(
        attempt_id=attempt_id
    ).all()

    return {
        response.question_id
        for response in responses
    }