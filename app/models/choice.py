from Online_Quiz_Platform.app.extensions import db


class Choice(db.Model):
    __tablename__ = "choice"

    id = db.Column(db.Integer, primary_key=True)

    question_id = db.Column(
        db.Integer,
        db.ForeignKey("question.id"),
        nullable=False
    )

    choice_text = db.Column(
        db.String(255),
        nullable=False
    )

    is_correct = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    # Relationship with Question
    question = db.relationship(
        "Question",
        back_populates="choices"
    )

    responses = db.relationship(
        "Response",
        back_populates="selected_choice",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Choice {self.choice_text}>"