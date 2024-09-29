from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes

from init import db
from models.workout import Workout, workout_schema, workouts_schema


# Create workout blueprint
workout_bp = Blueprint("workouts", __name__,url_prefix="/workouts")


# Method => GET, Route: /workouts/
# Route for users to see all their workout sessions, JWT required
@workout_bp.route("/")
@jwt_required()
def get_all_workouts():
    # Get the current user's identity from the JWT token
    current_user = get_jwt_identity()

    # Create and execute statement, filter by user's ID, order by desc date
    stmt = db.select(Workout).filter_by(user_id=current_user).order_by(Workout.date.desc())
    workouts = list(db.session.scalars(stmt))
    
    if workouts:
        # Serialize data using workouts_schema
        return workouts_schema.dump(workouts), 200
    else:
        # Else return error msg
        return {"Error": "No workout logs to display for this user."}, 400


# Method => GET, Route: /workouts/<workout_id>
# Route for users to see a specific workout session, JWT required
@workout_bp.route("/<int:workout_id>")
@jwt_required()
def get_a_workout(workout_id):
    # Use stmt and filter_by to select a specific workout
    stmt = db.select(Workout).filter_by(id=workout_id)
    workout = db.session.scalar(stmt)
    
    # If workout returns workout, Else returns error message
    if workout:
        return workout_schema.dump(workout), 200
    else:
        return {"error": f"Workout with {workout_id} not found."}, 404


# Method => POST, Route: /workouts/
# Route for users to create log their workout session
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
    except DataError:
        return {"error": "Invalid input for integer value, only numbers allowed."}, 400 
    except Exception as e:
        return {"error": f"An unexpected error had occurred, {e}"}


# Method => PATCH or PUT, Route: /workouts/<workout_id>
# Route for users to update their workout session, JWT required
@workout_bp.route("/<int:workout_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_workout(workout_id):
    try:
        # Get the fields from the body of the request, partial=True to update partial data
        body_data = workout_schema.load(request.get_json(), partial=True)
        stmt = db.select(Workout).filter_by(id=workout_id)
        workout = db.session.scalar(stmt)

        # Get the current user's identity from the JWT
        current_user_id = get_jwt_identity()

        # If workout exists, check ownership and edit required fields
        if workout:
            # Check if the current user is the owner of the workout
            # Convert values to int to ensure compatibility check
            if int(workout.user_id) != int(current_user_id):
                return {"error": "You do not have permission to update this workout."}, 403
            
            workout.title = body_data.get("title") or workout.title
            workout.distance_kms = body_data.get("distance_kms") or workout.distance_kms
            workout.calories_burnt = body_data.get("calories_burnt") or workout.calories_burnt
            
            # Commit changes to DB and return updated workout
            db.session.commit()
            return workout_schema.dump(workout)
        else:
            return {"error": f"Workout with id {workout_id} has not been found."}, 404
            
    # Return personalized error messages
    except DataError:
        return {"error": "Invalid input for integer value, only numbers allowed."}, 400 
    except Exception as e:
        return {"error": f"An unexpected error has occurred: {e}"}


# Route for users to delete their workout session, JWT required
@workout_bp.route("/<int:workout_id>", methods=["DELETE"])
@jwt_required()
def delete_workout(workout_id):
    # Fetch the workout from DB with stmt
    stmt = db.select(Workout).filter_by(id=workout_id)
    workout = db.session.scalar(stmt)
    
    # Get the current user's identity from the JWT 
    current_user_id = get_jwt_identity()
    
    # If workout exists, check ownership
    if workout:
        # Check if the current user is the owner of the workout
        if int(workout.user_id) != int(current_user_id):
            return {"error": "You do not have permission to delete this workout."}, 403    
    
        # If the user is the owner, delete the workout
        db.session.delete(workout)
        db.session.commit()
        return {"message": f"Workout {workout_id} has been deleted successfully!"}, 200
    else:
        return {"error": f"Workout {workout_id} has not been found."}, 404
