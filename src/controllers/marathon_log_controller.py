from datetime import date, datetime

from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from psycopg2 import errorcodes

from init import db
from models.marathon_log import Log, log_schema, logs_schema
from utils import auth_as_admin_decorator
from models.user import User
from models.group import Group
from models.marathon import Marathon

# Create marathon blueprint
log_bp = Blueprint("enroll", __name__,url_prefix="/<int:marathon_id>/logs")


# Route for admin to enrol their group in marathon event 
@log_bp.route("/", methods=["POST"])
@jwt_required()
@auth_as_admin_decorator
def marathon_registration(marathon_id):
    try:
        # Get the admin using JWT 
        admin_id = get_jwt_identity()
        admin_user = User.query.get(admin_id) 

        # Get the group associated with the admin
        group = Group.query.get(admin_user.group_id)
        if not group:
            return {"error": "You don't have a group to enrol, please create a group first."}, 404

        # Check if the marathon exists
        marathon = Marathon.query.get(marathon_id)
        if not marathon:
            return {"error": "Marathon doesn't exist, please choose an available event."}, 404
        
        # Check if the group is already signed up for this marathon
        existing_log = Log.query.filter_by(group_id=group.id, marathon_id=marathon_id).first()
        if existing_log:
            return {"error": f"This group is already enrolled in this marathon."}, 400

        # Create the log entry
        log_entry = Log(
            entry_created=date.today(),
            group_id=group.id,
            marathon_id=marathon_id  
        )

        # Add the log entry to the DB
        db.session.add(log_entry)
        db.session.commit()

        # Return marathon log
        return log_schema.dump(log_entry), 201

    # Handle DB and any possible errors
    except SQLAlchemyError as e:
        return {"error": "A database error has occurred. Please try again."}, 500
    except Exception as e:
         return {"error": f"An error has occurred: {e}"}, 500   


# Route for admin to remove their group from marathon event
@log_bp.route("/<int:log_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin_decorator
def delete_log(marathon_id, log_id):
    try:
        # Fetch the log entry and ensure it belongs to the correct marathon
        log = Log.query.filter_by(id=log_id, marathon_id=marathon_id).first()

        # If not log return error msg
        if not log:
            return {"message": f"Log with id {log_id} in marathon {marathon_id} was not found."}, 404

        # Fetch group and marathon info for a more descriptive return message
        group = Group.query.get(log.group_id)
        marathon = Marathon.query.get(marathon_id)

        # If not group or marathon return error msg
        if not group or not marathon:
            return {"message": "Error retrieving group or marathon information."}, 404

        # Delete the log
        db.session.delete(log)
        db.session.commit()

        # Return acknowledgment msg
        return {"message": f"{group.name} with ID {group.id} has been successfully removed from {marathon.name} event."}, 200
    
    # Handle DB and any possible errors
    except SQLAlchemyError as e:
        return {"error": "A database error has occurred. Please try again."}, 500
    except Exception as e:
         return {"error": f"An error has occurred: {e}"}, 500  













