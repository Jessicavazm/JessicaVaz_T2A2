from datetime import date, datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes

from init import db
from models.marathon import Marathon, marathon_schema, marathons_schema
from models.user import User
from utils import auth_as_admin_decorator
from controllers.marathon_log_controller import marathon_signup_bp

# Create Marathon bp
marathon_bp = Blueprint("marathons", __name__,url_prefix="/marathons")
# Register marathon_signup bp
marathon_bp.register_blueprint(marathon_signup_bp)


# GET method => /marathons
# Route for users and admins to see all marathons 
@marathon_bp.route("/")
def get_all_marathons():
    # Fetch marathons from DB
    stmt = db.select(Marathon).order_by(Marathon.name.asc())
    marathons = list(db.session.scalars(stmt))
    
    if marathons:
        # Serialise data using marathons_schema
        return marathons_schema.dump(marathons), 200
    # Else returns error msg
    else:
        return {"Error": "No marathons created yet."}, 400


# GET method => /marathons/<marathon_id>
# Route for users and admins to see a specific marathon
@marathon_bp.route("/<int:marathon_id>")
@jwt_required()
def get_a_marathon(marathon_id):
    # filter_by to select a specific workout
    stmt = db.select(Marathon).filter_by(id=marathon_id)
    marathon = db.session.scalar(stmt)
    
    # If marathon returns it, Else returns error msg
    if marathon:
        return marathon_schema.dump(marathon)
    else:
        return {"error": f"Marathon with {marathon_id} not found."}, 404


# POST method => /marathons/register
# Route for admins to create marathons, more than one allowed per admin.
@marathon_bp.route("/register", methods=["POST"])
@jwt_required()
@auth_as_admin_decorator
def register_marathon():
    try:
        # Get the fields from the body of the request, deserialize using marathon_schema
        body_data = marathon_schema.load(request.get_json())
        # Fetch date and store in marathon_date variable
        marathon_date_str = body_data.get("event_date")
        # Convert str into date object, Format YYYY-MM-DD
        marathon_date = datetime.strptime(marathon_date_str, '%Y-%m-%d').date()
        
        # Check date validation, return error msg if past date
        if marathon_date <= date.today():
            return {"error": "The marathon date must be in the future."}, 400

        # Create a new marathon instance
        marathon = Marathon(
            name=body_data.get("name"),
            event_date=marathon_date,
            location=body_data.get("location"),
            distance_kms=body_data.get("distance_kms")
        )
       
        # Add and commit to the DB
        db.session.add(marathon)
        db.session.commit()
        # Return acknowledgment message
        return marathon_schema.dump(marathon), 201
    # Return personalised msgs for data violations and invalid data
    except DataError:
        return {"error": "Invalid input for integer value, only numbers allowed."}, 400 
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return{"error": f"The column {err.orig.diag.column_name} is required"}, 400
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD."}, 400


# PUT/PATCH methods => /marathons/<marathon_id>
# Route for admins to update marathons events, 
# All admins are allowed to update info on marathon events.
@marathon_bp.route("/<int:marathon_id>", methods=["PUT", "PATCH"])
@jwt_required()
@auth_as_admin_decorator
def update_marathon(marathon_id):
    # Fetch fields from body of request
    body_data = marathon_schema.load(request.get_json(), partial=True)
    stmt = db.select(Marathon).filter_by(id=marathon_id)
    marathon = db.session.scalar(stmt)

    # Error msg if marathon is not found
    if not marathon:
        return {"error": f"Marathon with ID {marathon_id} has not been found."}, 404

    # Update fields
    marathon.name = body_data.get("name", marathon.name)
    marathon.location = body_data.get("location", marathon.location)
    marathon.distance_kms = body_data.get("distance_kms", marathon.distance_kms)

    # Update and validate the date if provided
    if "date" in body_data:
        try:
            marathon.date = datetime.strptime(body_data["date"], '%Y-%m-%d').date()
            if marathon.date <= date.today():
                return {"error": "The marathon date must be in the future."}, 400
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD."}, 400

    # Commit changes to DB and handle potential errors
    try:
        db.session.commit()
        return marathon_schema.dump(marathon), 200
    except DataError:
        return {"error": "Invalid input for integer value, only numbers allowed."}, 400
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 400


# Route for admin to delete marathon event
# All admins are allowed to delete the marathons events
@marathon_bp.route("/<int:marathon_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin_decorator
def delete_marathon(marathon_id):
    # Fetch the marathon from DB with stmt
    stmt = db.select(Marathon).filter_by(id=marathon_id)
    marathon = db.session.scalar(stmt)
    
    # If marathon exist delete it, ELSE returns error message
    if marathon:    
        db.session.delete(marathon)
        db.session.commit()
        return {"message": f"{marathon.name} event has been deleted successfully!"}, 200
    else:
        return {"error": f"Marathon with ID {marathon_id} has been not found."}, 404
    

