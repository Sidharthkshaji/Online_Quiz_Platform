from datetime import datetime

from Online_Quiz_Platform.app.extensions import db


class Question(db.Model):
    __tablename__ = "question"

    id = db.Column(db.Integer, primary_key=True)

    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey("quiz.id"),
        nullable=False
    )

    question_text = db.Column(
        db.Text,
        nullable=False
    )

    marks = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationship with Quiz
    quiz = db.relationship(
        "Quiz",
        back_populates="questions"
    )

    # Relationship with Choice
    choices = db.relationship(
        "Choice",
        back_populates="question",
        cascade="all, delete-orphan",
        lazy=True
    )

    responses = db.relationship(
        "Response",
        back_populates="question",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Question {self.id}>"