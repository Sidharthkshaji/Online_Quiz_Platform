import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.category import Category
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.choice import Choice


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def test_user_loader(app):
    from app import load_user
    user = User(name="Test User", username="testuser", email="test@example.com")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()

    loaded = load_user(str(user.id))
    assert loaded is not None
    assert loaded.email == "test@example.com"

    invalid_user = load_user("invalid")
    assert invalid_user is None


def test_question_choices_ordering(app):
    user = User(name="Admin", username="admin", email="admin@example.com", role="admin")
    user.set_password("password123")
    category = Category(name="General", description="General category")
    db.session.add_all([user, category])
    db.session.commit()

    quiz = Quiz(
        title="Sample Quiz",
        category_id=category.id,
        difficulty="Easy",
        time_limit=10,
        created_by=user.id
    )
    db.session.add(quiz)
    db.session.commit()

    question = Question(quiz_id=quiz.id, question_text="What is 2+2?", marks=1)
    db.session.add(question)
    db.session.commit()

    c1 = Choice(question_id=question.id, choice_text="4", is_correct=True)
    c2 = Choice(question_id=question.id, choice_text="3", is_correct=False)
    db.session.add_all([c1, c2])
    db.session.commit()

    refreshed_question = db.session.get(Question, question.id)
    choices = refreshed_question.choices
    assert choices[0].id < choices[1].id
    assert choices[0].choice_text == "4"
