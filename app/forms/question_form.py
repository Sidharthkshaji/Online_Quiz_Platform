from flask_wtf import FlaskForm
from wtforms import (
    TextAreaField,
    StringField,
    IntegerField,
    RadioField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange
)


class QuestionForm(FlaskForm):

    question_text = TextAreaField(
        "Question",
        validators=[
            DataRequired(),
            Length(min=5, max=500)
        ]
    )

    marks = IntegerField(
        "Marks",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=100)
        ],
        default=1
    )

    choice_a = StringField(
        "Choice A",
        validators=[
            DataRequired(),
            Length(max=255)
        ]
    )

    choice_b = StringField(
        "Choice B",
        validators=[
            DataRequired(),
            Length(max=255)
        ]
    )

    choice_c = StringField(
        "Choice C",
        validators=[
            DataRequired(),
            Length(max=255)
        ]
    )

    choice_d = StringField(
        "Choice D",
        validators=[
            DataRequired(),
            Length(max=255)
        ]
    )

    correct_choice = RadioField(
        "Correct Choice",
        choices=[
            ("A", "Choice A"),
            ("B", "Choice B"),
            ("C", "Choice C"),
            ("D", "Choice D")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Save Question")