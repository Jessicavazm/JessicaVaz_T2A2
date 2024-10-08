# Os for fetching env variables
import os

# To create the API
from flask import Flask
# To handle Validation errors
from marshmallow.exceptions import ValidationError

# Import objects from init.py
from init import db, ma, bcrypt, jwt
# Import blueprints to register them in the app
from controllers.cli_controllers import db_commands
from controllers.auth_controller import auth_bp
from controllers.workout_controller import workout_bp
from controllers.group_controller import group_bp
from controllers.marathon_controller import marathon_bp


# Define the app inside of an application factory function
def  create_app():
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    # Initialise app with extensions
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    

    # Global decorators to handle errors
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {"error": err.messages}, 400
    
    @app.errorhandler(400)
    def handle_bad_request(err):
        return{"error": "Bad request. Please check your input."}, 400

    @app.errorhandler(401)
    def unauthorised(error):
        return {"error": "You are not an authorised user."}, 401
    
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "The requested resource was not found."}, 404
    
    @app.errorhandler(405)
    def not_found(error):
        return {"error": "The requested method is not allowed."}, 405
    
    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "An unexpected error occurred on the server."}, 500


    # Register blueprints
    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)
    app.register_blueprint(workout_bp)
    app.register_blueprint(group_bp)
    app.register_blueprint(marathon_bp)


    return app
