from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from psycopg2 import errorcodes

from init import db
from models.marathon import Marathon, MarathonSchema, marathon_schema, marathons_schema
from models.user import User
from utils import auth_as_admin_decorator

# Create marathon blueprint
marathon_bp = Blueprint("marathon", __name__,url_prefix="/marathon")

@marathon_bp.route("/")
def get_all_marathons():
    # Create and execute stmt, order by asc order
    # Convert marathon to list to use IF statement 
    stmt = db.select(Marathon).order_by(Marathon.name.asc())
    marathons = list(db.session.scalars(stmt))
    if marathons:
        # Serialise data using marathons_schema
        return marathons_schema.dump(marathons), 200
    # Else returns error message
    else:
        return {"Error": "No marathons to display."}, 400
    

# Create 'register' marathon route,'POST' method to insert data into DB
# Auth_as_admin decorator only allows admin to create marathons
@marathon_bp.route("/register", methods=["POST"])
@jwt_required()
@auth_as_admin_decorator
def register_marathon():
    try:
        # Get the fields from the body of the request, deserialize using marathon_schema
        body_data = marathon_schema.load(request.get_json())

        # Create a new marathon instance
        marathon = Marathon(
            name=body_data.get("name"),
            date=date.today(),
            location=body_data.get("location"),
            distance_kms=body_data.get("distance_kms")
        )
        # Add and commit to the DB
        db.session.add(marathon)
        db.session.commit()
        # Return acknowledgment message
        return marathon_schema.dump(marathon), 201
    # Return not null violation personalised message   
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return{"error": f"The column {err.orig.diag.column_name} is required"}, 400


# Create route for updating marathon JWT required
# @auth_as_admin to only authorise admins to perform this
@marathon_bp.route("/<int:marathon_id>", methods = ["PUT", "PATCH"])
@jwt_required()
@auth_as_admin_decorator
def update_marathon(marathon_id):
    # Get the fields from body of the request, partial=True to update partial data
    body_data = marathon_schema.load(request.get_json(), partial=True)
    stmt = db.select(Marathon).filter_by(id=marathon_id)
    marathon = db.session.scalar(stmt)
    # If marathon exist, edit required fields, ELSE returns error message
    if marathon:
        marathon.name = body_data.get("name") or marathon.name
        marathon.date = body_data.get("date") or marathon.date
        marathon.location = body_data.get("location") or marathon.location
        marathon.distance_kms = body_data.get("distance_kms") or marathon.distance_kms
        # Commit changes to DB, return updated marathon
        db.session.commit()
        return marathon_schema.dump(marathon)
    else:
        return {"error": f"Marathon with id {marathon_id} has not been found."}, 404


# Create route for deleting marathon, JWT required
# @auth_as_admin to only authorise admins to perform this
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
        return {"message": f"Marathon {marathon_id} has been deleted successfully!"}, 200
    else:
        return {"error": f"Marathon {marathon_id} has been not found."}, 404