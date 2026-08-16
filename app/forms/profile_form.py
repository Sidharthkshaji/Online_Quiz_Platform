from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    FileField
)
from wtforms.validators import (
    DataRequired,
    Length,
    EqualTo,
    ValidationError,
    Optional
)

from flask_login import current_user
from app.models.user import User


class ProfileEditForm(FlaskForm):

    name = StringField(
        "Full Name",
        validators=[
            DataRequired(
                message="Full name is required."
            ),
            Length(
                min=2,
                max=100,
                message="Name must be between 2 and 100 characters."
            )
        ]
    )

    username = StringField(
        "Username",
        validators=[
            DataRequired(
                message="Username is required."
            ),
            Length(
                min=3,
                max=50,
                message="Username must be between 3 and 50 characters."
            )
        ]
    )

    profile_photo = FileField(
        "Profile Photo",
        validators=[Optional()]
    )

    current_password = PasswordField(
        "Current Password",
        validators=[Optional()]
    )

    new_password = PasswordField(
        "New Password",
        validators=[
            Optional(),
            Length(
                min=8,
                message="Password must be at least 8 characters."
            )
        ]
    )

    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            EqualTo(
                "new_password",
                message="Passwords must match."
            )
        ]
    )

    submit = SubmitField("Save Changes")

    def validate_username(self, username):

        value = username.data.strip().lstrip("@").lower()

        username.data = value

        import re

        if not re.fullmatch(
            r"[a-z0-9._]+",
            value
        ):
            raise ValidationError(
                "Username can contain only letters, numbers, dots and underscores."
            )

        existing_user = User.query.filter(
            User.username == value,
            User.id != current_user.id
        ).first()

        if existing_user:

            raise ValidationError(
                "That username is already taken. Please choose another."
            )

    def validate_new_password(self, new_password):

        if new_password.data:

            if not self.current_password.data:

                raise ValidationError(
                    "Please enter your current password to change your password."
                )

            if not current_user.check_password(
                self.current_password.data
            ):

                raise ValidationError(
                    "Current password is incorrect."
                )