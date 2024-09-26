from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.group import Group, group_schema, groups_schema
from models.user import User
from models.group_log import GroupLog
from controllers.group_log_controller import group_signup_bp
from utils import auth_as_admin_decorator, admin_group_check_decorator


# Group BP
group_bp = Blueprint("groups", __name__, url_prefix="/groups")
# Register group_sign_bp
group_bp.register_blueprint(group_signup_bp)


# Route to see all groups
@group_bp.route("/")
def get_all_groups():
    # Create and execute stmt, order by asc order
    stmt = db.select(Group).order_by(Group.name.asc())
    groups = list(db.session.scalars(stmt))
    if groups:
        # Serialize data using groups_schema
        return groups_schema.dump(groups), 200
    # else error msg
    else:
        return {"Error": "No groups to display."}, 400


# Route to see specific group
@group_bp.route("/<int:group_id>")
def get_a_group(group_id):
    # Use stmt and filter_by to select a specific group
    stmt = db.select(Group).filter_by(id=group_id)
    group = db.session.scalar(stmt)
    # If group exists, return it, else return error msg
    if group:
        return group_schema.dump(group), 200
    else:
        return {"error": f"Group with {group_id} not found."}, 404


# Route to create a group
@group_bp.route("/", methods=["POST"])
@jwt_required()
@auth_as_admin_decorator
@admin_group_check_decorator
def create_a_group():
    try:
        # Get the fields from the request and create a new group
        body_data = group_schema.load(request.get_json())
        group = Group(
            name=body_data.get("name"),
            date_created=date.today()
        )

        # Add the new group to the database
        db.session.add(group)
        db.session.commit()

        # Log the changes in GroupLog
        group_log = GroupLog(user_id=get_jwt_identity(), group_id=group.id)
        db.session.add(group_log)
        db.session.commit()

        # Return the created group
        return group_schema.dump(group), 201
    except Exception as e:
        return {"error": f"An unexpected error has ocurred, {e}."}
    

# Route for admins to update their group
@group_bp.route("/<int:group_id>", methods=["PUT", "PATCH"])
@jwt_required()
@auth_as_admin_decorator
def update_group(group_id):
    # Get the fields from the body of the request, partial=True to update partial data
    body_data = group_schema.load(request.get_json(), partial=True)
    stmt = db.select(Group).filter_by(id=group_id)
    group = db.session.scalar(stmt)
    
    # If group exists, edit the required fields, else return error message
    if group:
        group.name = body_data.get("name") or group.name
        # Commit changes to DB, return updated group
        db.session.commit()
        return group_schema.dump(group), 200
    else:
        return {"error": f"Group with id {group_id} has not been found."}, 404


# Route for admin to delete their group
@group_bp.route("/<int:group_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin_decorator
def delete_group(group_id):
    # Fetch the group from the DB with stmt
    stmt = db.select(Group).filter_by(id=group_id)
    group = db.session.scalar(stmt)
    
    # If group exists, delete it, else return error message
    if group:
        db.session.delete(group)
        db.session.commit()
        return {"message": f"Group {group.id} has been deleted successfully!"}, 200
    else:
        return {"error": f"Group {group_id} has not been found."}, 404

