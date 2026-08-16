import os
import uuid

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.utils import secure_filename

from PIL import (
    Image,
    ImageOps
)

from app.services.dashboard_service import (
    get_admin_dashboard_data,
    get_student_dashboard_data
)

from app.forms.profile_form import ProfileEditForm
from app.extensions import db


ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}


main = Blueprint(
    "main",
    __name__
)


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


@main.route("/")
def home():

    return render_template(
        "home.html"
    )


@main.route("/dashboard")
@login_required
def dashboard():

    if current_user.is_admin:

        data = get_admin_dashboard_data()

        return render_template(
            "dashboard/admin_dashboard.html",
            **data
        )

    data = get_student_dashboard_data(
        current_user.id
    )

    return render_template(
        "dashboard/student_dashboard.html",
        **data
    )


@main.route(
    "/profile",
    methods=["GET", "POST"]
)
@login_required
def profile():

    form = ProfileEditForm()

    if form.validate_on_submit():

        current_user.name = (
            form.name.data.strip()
        )

        current_user.username = (
            form.username.data.strip()
            .lstrip("@")
            .lower()
        )

        # -----------------------------------------
        # PROFILE PHOTO
        # -----------------------------------------

        if form.profile_photo.data:

            file = form.profile_photo.data

            if not allowed_file(
                file.filename
            ):

                flash(
                    "Please upload a PNG, JPG, JPEG or WEBP image.",
                    "danger"
                )

                return redirect(
                    url_for("main.profile")
                )

            try:

                image = Image.open(file)

                # Verify that it is a real image
                image.verify()

                # Re-open after verify()
                file.seek(0)

                image = Image.open(file)

                image = ImageOps.exif_transpose(
                    image
                )

                # Convert transparent images
                # to RGB with a white background
                if image.mode in (
                    "RGBA",
                    "LA"
                ):

                    background = Image.new(
                        "RGB",
                        image.size,
                        "white"
                    )

                    background.paste(
                        image,
                        mask=image.getchannel("A")
                    )

                    image = background

                else:

                    image = image.convert(
                        "RGB"
                    )

                # Crop to a perfect square
                # and resize to standard avatar size
                image = ImageOps.fit(
                    image,
                    (512, 512),
                    method=Image.Resampling.LANCZOS,
                    centering=(0.5, 0.5)
                )

                upload_dir = os.path.join(
                    current_app.root_path,
                    "static",
                    "uploads",
                    "profiles"
                )

                os.makedirs(
                    upload_dir,
                    exist_ok=True
                )

                filename = (
                    f"{current_user.id}_"
                    f"{uuid.uuid4().hex}.jpg"
                )

                filepath = os.path.join(
                    upload_dir,
                    filename
                )

                image.save(
                    filepath,
                    "JPEG",
                    quality=90,
                    optimize=True
                )

                # Delete old photo
                if current_user.profile_photo:

                    old_photo = os.path.join(
                        current_app.root_path,
                        "static",
                        current_user.profile_photo
                    )

                    if os.path.exists(
                        old_photo
                    ):

                        os.remove(
                            old_photo
                        )

                current_user.profile_photo = (
                    f"uploads/profiles/{filename}"
                )

            except Exception:

                flash(
                    "The uploaded file is not a valid image.",
                    "danger"
                )

                return redirect(
                    url_for("main.profile")
                )

        # -----------------------------------------
        # PASSWORD
        # -----------------------------------------

        if form.new_password.data:

            current_user.set_password(
                form.new_password.data
            )

        db.session.commit()

        flash(
            "Your profile has been updated successfully.",
            "success"
        )

        return redirect(
            url_for("main.profile")
        )

    elif not form.is_submitted():

        form.name.data = current_user.name
        form.username.data = current_user.username

    return render_template(
        "profile.html",
        form=form,
        user=current_user
    )