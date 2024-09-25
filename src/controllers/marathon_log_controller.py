from datetime import date

from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from psycopg2 import errorcodes

from init import db

from models.marathon_log import MarathonLog, marathon_log_schema
from models.user import User
from models.group import Group
from models.marathon import Marathon
from models.group_log import GroupLog
from utils import auth_as_admin_decorator


# Create marathon sign up blueprint
marathon_signup_bp = Blueprint("signup", __name__,url_prefix="/<int:marathon_id>/signup")


# Route for admin to enrol their group in marathon events
# marathons/<marathon_id>/signup
@marathon_signup_bp.route("/", methods=["POST"])
@jwt_required()
@auth_as_admin_decorator
def marathon_registration(marathon_id):
    try:
        # Get the admin user ID from the JWT token
        admin_id = get_jwt_identity()

        # Retrieve group logs associated with the admin user
        group_logs = GroupLog.query.filter_by(user_id=admin_id).all()
        
        # If not group, instruct admin to create group first
        if not group_logs:
            return {"error": "You don't have a group to enroll, please create a group first."}, 404

        # Get the first group from the user's group logs
        group = Group.query.get(group_logs[0].group_id)

        # Check if the specified marathon exists
        marathon = Marathon.query.get(marathon_id)
        if not marathon:
            return {"error": "Marathon doesn't exist, please choose an available event."}, 404
        
        # Check if the group is already signed up for this marathon
        existing_log = MarathonLog.query.filter_by(group_id=group.id, marathon_id=marathon_id).first()
        if existing_log:
            return {"error": "This group is already enrolled in this marathon."}, 400

        # Create a new log entry for the marathon
        log_entry = MarathonLog(
            entry_created=date.today(),  
            group_id=group.id,           
            marathon_id=marathon_id       
        )

        # Add the log entry to the database session
        db.session.add(log_entry)
        db.session.commit()  

        # Return marathon entry
        return marathon_log_schema.dump(log_entry), 201

    # Handle DB and any possible errors
    except SQLAlchemyError:
        return {"error": "A database error has occurred. Please try again."}, 500
    except Exception as e:
        return {"error": f"An error has occurred: {e}"}, 500 
   

# Route for admin to remove their group from marathon event
# /<marathon_id>/signup/logs/<log_id>
@marathon_signup_bp.route("/logs/<int:log_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin_decorator
def delete_log(marathon_id, log_id):
    try:
        # Fetch the log entry and ensure it belongs to the correct marathon
        log = MarathonLog.query.filter_by(id=log_id, marathon_id=marathon_id).first()

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













