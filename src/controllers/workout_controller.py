from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from models.workout import Workout, workout_schema, workouts_schema, WorkoutSchema
from init import db, bcrypt


# Create workout blueprint
workout_bp = Blueprint("workout", __name__,url_prefix="/workout")


# Create route for 'GET' workouts
@workout_bp.route("/")
def get_all_workouts():
    # Create and execute stmt, order by descending order
    stmt = db.select(Workout).order_by(Workout.date.desc())
    workouts = db.session.scalars(stmt)
    # Serialise data using workouts_schema
    return workouts_schema.dump(workouts), 200


# Create route for 'GET' a specific workout
@workout_bp.route("/<int:workout_id>")
def get_a_workout(workout_id):
    # Use filter_by to select a specific card
    # stmt = db.select(Card).where(Card.id==card_id)
    stmt = db.select(Workout).filter_by(id=workout_id)
    workout = db.session.scalar(stmt)
    # If workout returns workout, Else returns error message
    if workout:
        return workout_schema.dump(workout)
    else:
        return {"error": f"Card with {workout_id} not found."}, 404


# Create 'register' workout route, JWT required, 'POST' method to insert data into DB
@workout_bp.route("/", methods=["POST"])
@jwt_required()
def register_workout():
    try:
        # Get the fields from the body of the request, deserialize using workout_schema
        body_data = workout_schema.load(request.get_json())

        # Create a new workout instance
        workout = Workout(
            title=body_data.get("title"),
            date=date.today(),
            distance_kms=body_data.get("distance_kms"),
            calories_burnt=body_data.get("calories_burnt"),
            user_id=get_jwt_identity()
        )
        # Add and commit to the DB
        db.session.add(workout)
        db.session.commit()
        # Return acknowledgment message
        return workout_schema.dump(workout), 201
    # Return not null violation personalised message   
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return{"error": f"The column {err.orig.diag.column_name} is required"}, 400


# Create route for updating workout, JWT required
@workout_bp.route("/<int:workout_id>", methods = ["PUT", "PATCH"])
@jwt_required()
def update_workout(workout_id):
# Get the fields from body of the request, partial=True to update partial data
    body_data = workout_schema.load(request.get_json(), partial=True)
    stmt = db.select(Workout).filter_by(id=workout_id)
    workout = db.session.scalar(stmt)
    # If workout exist, edit required fields, ELSE returns error message
    if workout:
        workout.title = body_data.get("title") or workout.title
        workout.distance_kms = body_data.get("distance_kms") or workout.distance_kms
        workout.calories_burnt = body_data.get("calories_burnt") or workout.calories_burnt
        # Commit changes to DB, return updated workout
        db.session.commit()
        return workout_schema.dump(workout)
    else:
        return {"error": f"Workout with id {workout_id} has not been found."}, 404


# Create route for deleting workout, JWT required
@workout_bp.route("/<int:workout_id>", methods=["DELETE"])
@jwt_required()
def delete_card(workout_id):
    # Fetch the workout from DB with stmt
    stmt = db.select(Workout).filter_by(id=workout_id)
    workout = db.session.scalar(stmt)
    # If workout exist delete it, ELSE returns error message
    if workout:    
        db.session.delete(workout)
        db.session.commit()
        return {"message": f"Workout {workout_id} has been deleted successfully!"}, 200
    else:
        return {"error": f"Workout {workout_id} has been not found."}, 404