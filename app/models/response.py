from app.extensions import db


class Response(db.Model):
    __tablename__ = "response"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    attempt_id = db.Column(
        db.Integer,
        db.ForeignKey("attempt.id"),
        nullable=False
    )

    question_id = db.Column(
        db.Integer,
        db.ForeignKey("question.id"),
        nullable=False
    )

    selected_choice_id = db.Column(
        db.Integer,
        db.ForeignKey("choice.id"),
        nullable=False
    )

    attempt = db.relationship(
        "Attempt",
        back_populates="responses"
    )

    question = db.relationship(
        "Question",
        back_populates="responses"
    )

    selected_choice = db.relationship(
        "Choice",
        back_populates="responses"
    )

    def __repr__(self):
        return f"<Response {self.id}>"