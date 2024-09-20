import os
from flask import Flask

# Import objects from init.py
from init import db, ma, bcrypt, jwt
# Import blueprints to register them in the app
from controllers.cli_controllers import db_commands
from controllers.auth_controller import auth_bp


# Define the app inside of an application factory function
def  create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    

    # Register blueprints
    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)

    return app
