from Online_Quiz_Platform.app.extensions import db
from Online_Quiz_Platform.app.models.quiz import Quiz
from Online_Quiz_Platform.app.models.category import Category


def get_all_quizzes():
    """
    Return all quizzes ordered by title.
    """
    return Quiz.query.order_by(Quiz.title).all()


def get_quiz_by_id(quiz_id):
    """
    Return a quiz by its ID.
    """
    return Quiz.query.get_or_404(quiz_id)


def get_category_choices():
    """
    Returns categories for the SelectField.
    Example:
    [(1, "Python"), (2, "Java")]
    """
    categories = Category.query.order_by(Category.name).all()

    return [(category.id, category.name) for category in categories]


def create_quiz(title,
                description,
                category_id,
                difficulty,
                time_limit,
                created_by):
    """
    Create a new quiz.
    """

    quiz = Quiz(
        title=title,
        description=description,
        category_id=category_id,
        difficulty=difficulty,
        time_limit=time_limit,
        created_by=created_by
    )

    db.session.add(quiz)
    db.session.commit()

    return True, "Quiz created successfully."


def update_quiz(quiz,
                title,
                description,
                category_id,
                difficulty,
                time_limit):

    quiz.title = title
    quiz.description = description
    quiz.category_id = category_id
    quiz.difficulty = difficulty
    quiz.time_limit = time_limit

    db.session.commit()

    return True, "Quiz updated successfully."


def delete_quiz(quiz):

    db.session.delete(quiz)
    db.session.commit()

    return True, "Quiz deleted successfully."