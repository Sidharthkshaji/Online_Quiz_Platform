from flask import Flask

from Online_Quiz_Platform.app.config import Config
from Online_Quiz_Platform.app.extensions import db, migrate, login_manager


@login_manager.user_loader
def load_user(user_id):
    from Online_Quiz_Platform.app.models.user import User
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from Online_Quiz_Platform.app.models.user import User
    from Online_Quiz_Platform.app.models.category import Category
    from Online_Quiz_Platform.app.models.quiz import Quiz
    from Online_Quiz_Platform.app.models.question import Question
    from Online_Quiz_Platform.app.models.choice import Choice
    from Online_Quiz_Platform.app.models.attempt import Attempt
    from Online_Quiz_Platform.app.models.response import Response

    from Online_Quiz_Platform.app.routes.auth import auth
    from Online_Quiz_Platform.app.routes.main import main
    from Online_Quiz_Platform.app.routes.admin import admin
    from Online_Quiz_Platform.app.routes.student import student

    

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(student)


    return app