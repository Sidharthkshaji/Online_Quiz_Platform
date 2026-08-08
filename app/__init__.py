from flask import Flask

from app.config import Config
from app.extensions import db, migrate, login_manager


@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models.user import User
    from app.models.category import Category
    from app.models.quiz import Quiz
    from app.models.question import Question
    from app.models.choice import Choice
    from app.models.attempt import Attempt
    from app.models.response import Response

    from app.routes.auth import auth
    from app.routes.main import main
    from app.routes.admin import admin
    from app.routes.student import student

    

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(student)


    return app