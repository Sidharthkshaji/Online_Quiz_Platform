from app.extensions import db
from app.models.question import Question
from app.models.choice import Choice
from app.models.quiz import Quiz


def get_questions_by_quiz(quiz_id):
    """
    Return all questions belonging to a quiz.
    """
    return Question.query.filter_by(
        quiz_id=quiz_id
    ).all()


def get_question_by_id(question_id):
    """
    Return a question by ID.
    """
    return Question.query.get_or_404(question_id)


def create_question(
    quiz_id,
    question_text,
    marks,
    choice_a,
    choice_b,
    choice_c,
    choice_d,
    correct_choice
):
    """
    Create a question with four choices.
    """

    quiz = Quiz.query.get_or_404(quiz_id)

    question = Question(
        quiz_id=quiz.id,
        question_text=question_text,
        marks=marks
    )

    db.session.add(question)
    db.session.flush()

    choices = [
        Choice(
            question_id=question.id,
            choice_text=choice_a,
            is_correct=(correct_choice == "A")
        ),
        Choice(
            question_id=question.id,
            choice_text=choice_b,
            is_correct=(correct_choice == "B")
        ),
        Choice(
            question_id=question.id,
            choice_text=choice_c,
            is_correct=(correct_choice == "C")
        ),
        Choice(
            question_id=question.id,
            choice_text=choice_d,
            is_correct=(correct_choice == "D")
        )
    ]

    db.session.add_all(choices)

    # Update quiz statistics
    quiz.total_questions += 1

    db.session.commit()

    return True, "Question created successfully."


def update_question(
    question,
    question_text,
    marks,
    choice_a,
    choice_b,
    choice_c,
    choice_d,
    correct_choice
):
    """
    Update a question and its four choices.
    """

    question.question_text = question_text
    question.marks = marks

    choices = question.choices

    choices[0].choice_text = choice_a
    choices[1].choice_text = choice_b
    choices[2].choice_text = choice_c
    choices[3].choice_text = choice_d

    choices[0].is_correct = (correct_choice == "A")
    choices[1].is_correct = (correct_choice == "B")
    choices[2].is_correct = (correct_choice == "C")
    choices[3].is_correct = (correct_choice == "D")

    db.session.commit()

    return True, "Question updated successfully."

def delete_question(question):
    """
    Delete a question and update quiz statistics.
    """

    quiz = question.quiz

    db.session.delete(question)

    if quiz.total_questions > 0:
        quiz.total_questions -= 1

    db.session.commit()

    return True, "Question deleted successfully."