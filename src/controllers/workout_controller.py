from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.workout import Workout, workout_schema, WorkoutSchema
from init import db, bcrypt

from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

# Create workout blueprint
workout_bp = Blueprint("workout", __name__,url_prefix="/workout")


# Create 'register'  workout route, JWT required
@workout_bp.route("/register", methods=["POST"])
@jwt_required()
def register_workout():
    try:
        # Get the fields from body of request
        body_data = workout_schema.load(request.get_json())
        # Create a new workout instance
        workout = Workout(
            title = body_data.get("title"),
            date = date.today(),
            distance_kms = body_data.get("distance_kms"),
            calories_burnt = body_data.get("calories_burnt"),
            user_id = get_jwt_identity()
        )
        # Add and commit to DB
        db.session.add(workout)
        db.session.commit()
        # Return acknowledgment message
        return workout_schema.dump(workout), 201
    except IntegrityError as err:
        # Display personalised messages in case of data violations
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return{"error": f"The column {err.orig.diag.column_name} is required"}, 400
    

