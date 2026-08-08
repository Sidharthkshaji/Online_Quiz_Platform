from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    IntegerField,
    SelectField,
    SubmitField
)
from wtforms.validators import DataRequired, Length, NumberRange


class QuizForm(FlaskForm):

    title = StringField(
        "Quiz Title",
        validators=[
            DataRequired(),
            Length(min=3, max=150)
        ]
    )

    description = TextAreaField(
        "Description",
        validators=[
            Length(max=500)
        ]
    )

    category = SelectField(
        "Category",
        coerce=int,
        validators=[DataRequired()]
    )

    difficulty = SelectField(
        "Difficulty",
        choices=[
            ("Easy", "Easy"),
            ("Medium", "Medium"),
            ("Hard", "Hard")
        ],
        validators=[DataRequired()]
    )

    time_limit = IntegerField(
        "Time Limit (Minutes)",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=300)
        ]
    )

    submit = SubmitField("Save Quiz")