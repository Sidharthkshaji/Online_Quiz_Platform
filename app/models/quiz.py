from datetime import datetime

from Online_Quiz_Platform.app.extensions import db


class Quiz(db.Model):
    __tablename__ = "quiz"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id"),
        nullable=False
    )

    difficulty = db.Column(
        db.String(20),
        nullable=False
    )

    time_limit = db.Column(
        db.Integer,
        nullable=False
    )

    total_questions = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships
    category = db.relationship(
        "Category",
        back_populates="quizzes"
    )

    creator = db.relationship(
        "User",
        back_populates="quizzes_created"
    )

    questions = db.relationship(
        "Question",
        back_populates="quiz",
        cascade="all, delete-orphan",
        lazy=True
    )

    attempts = db.relationship(
        "Attempt",
        backref="quiz",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Quiz {self.title}>"