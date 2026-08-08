from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class CategoryForm(FlaskForm):
    name = StringField(
        "Category Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100)
        ]
    )

    description = TextAreaField(
        "Description",
        validators=[
            Length(max=500)
        ]
    )

    submit = SubmitField("Save Category")