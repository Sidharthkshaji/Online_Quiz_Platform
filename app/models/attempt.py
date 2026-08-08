from datetime import datetime

from app.extensions import db


class Attempt(db.Model):
    __tablename__ = "attempt"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey("quiz.id"),
        nullable=False
    )

    score = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    percentage = db.Column(
        db.Float,
        nullable=False,
        default=0.0
    )

    time_taken = db.Column(
        db.Integer,
        nullable=True
    )

    started_at = db.Column(
        db.DateTime,
        nullable=True,
        default=datetime.utcnow
    )

    submitted_at = db.Column(
        db.DateTime,
        nullable=True
    )

    responses = db.relationship(
        "Response",
        back_populates="attempt",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Attempt {self.id}>"