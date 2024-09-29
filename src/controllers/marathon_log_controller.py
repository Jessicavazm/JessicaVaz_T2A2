from datetime import date

from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from init import db
from models.marathon_log import MarathonLog, marathon_log_schema
from models.group import Group
from models.marathon import Marathon
from models.group_log import GroupLog
from utils import auth_as_admin_decorator


# Create marathon sign up blueprint
marathon_signup_bp = Blueprint("signup", __name__,url_prefix="/<int:marathon_id>")


# Route for admin to enrol their group in marathon event 
# marathons/<marathon_id>/signup
@marathon_signup_bp.route("/signup", methods=["POST"])
@jwt_required()
@auth_as_admin_decorator
def marathon_registration(marathon_id):
    try:
        # Get the admin user ID from the JWT token
        admin_id = get_jwt_identity()

        # Fetch the group associated with the admin (owner of the group)
        stmt = db.select(Group).filter_by(created_by=admin_id)
        group = db.session.scalar(stmt)
        
        # If no group exists, instruct the admin to create a group first
        if not group:
            return {"error": "You don't have a group to enroll, please create a group first."}, 404

        # Check if the specified marathon exists
        marathon = Marathon.query.get(marathon_id)
        if not marathon:
            return {"error": "The requested marathon doesn't exist, please choose an available event."}, 404
        
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

        # Return the marathon log entry
        return {marathon_log_schema.dump(log_entry), 201}

    # Handle DB and other possible errors
    except SQLAlchemyError:
        return {"error": "A database error has occurred. Please try again."}, 500
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}, 500


# Route for admin to remove their group from marathon event
# /<marathon_id>/logs/<log_id>
@marathon_signup_bp.route("/logs/<int:log_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin_decorator
def delete_log(marathon_id, log_id):
    # Get the admin user ID from the JWT token
    admin_id = get_jwt_identity()

    # Fetch the log entry
    log = MarathonLog.query.filter_by(id=log_id, marathon_id=marathon_id).first()

    # If no log found, return error msg
    if not log:
        return {"message": f"Log with id {log_id} in marathon {marathon_id} was not found."}, 404

    # Fetch the group associated with the log
    group = Group.query.get(log.group_id)

    # If no group found, return error msg
    if not group:
        return {"message": "Group associated with this log entry was not found."}, 404

    # Check if the current user is the owner of the group
    if int(group.created_by) != int(admin_id):
        return {"message": "You are not authorised to remove this group from the marathon event."}, 403

    # Delete the log entry
    db.session.delete(log)
    db.session.commit()

    # Return acknowledgment message
    return {"message": "Your group has been successfully removed from this event."}, 200














