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


# GET method => /groups
# Route for members to see all groups
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
        return {"Error": "No groups created yet."}, 400


# GET method => /groups/<group_id>
# Route for members to see a specific group
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


# POST method => /groups
# Route to create group (only admin allowed, one group per admin)
# @admin_group_check decorator ensure admin hasn't created a group yet
@group_bp.route("/", methods=["POST"])
@jwt_required()
@auth_as_admin_decorator
@admin_group_check_decorator
def create_a_group():
    try:
         # Get the current admin user_id from the JWT 
        user_id = get_jwt_identity()

        # Fetch the data from the body of request
        body_data = group_schema.load(request.get_json())
        
        # Create the new group and assign the admin as the creator 
        group = Group(
            name=body_data.get("name"),
            date_created=date.today(),
            created_by=user_id  
        )
        # Add the new group to DB, and return acknowledgment msg
        db.session.add(group)
        db.session.commit()

        # Return the created group
        return group_schema.dump(group), 201
    # Returns personalised msgs for data violation and general errors
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return{"error": f"The column {err.orig.diag.column_name} is required"}, 400
    except Exception as e:
        return {"error": f"An unexpected error has ocurred, {e}."}
    

# PUT, PATCH methods => /groups/<group_id>
# Route for admins to update their group
@group_bp.route("/<int:group_id>", methods=["PUT", "PATCH"])
@jwt_required()
@auth_as_admin_decorator
def update_group(group_id):
    # Get admin id and ensure they are associated with group
    user_id = get_jwt_identity()
    associated_group = GroupLog.query.filter_by(user_id=user_id, group_id=group_id).first()

    # If not owner, return error msg
    if not associated_group:
        return {"error": "You are not authorised to update this group."}, 403
    
    # Get the fields from the body of the request 
    # partial=True to update partial data
    body_data = group_schema.load(request.get_json(), partial=True)
    stmt = db.select(Group).filter_by(id=group_id)
    group = db.session.scalar(stmt)
    
    # If group exists, edit the required fields, else return error msg
    if group:
        group.name = body_data.get("name") or group.name
        # Commit changes to DB, return updated group
        db.session.commit()
        return group_schema.dump(group), 200
    else:
        return {"error": f"Group with id {group_id} has not been found."}, 404


# DELETE method => /groups/<group_id>
# Route for admin to delete their group
@group_bp.route("/<int:group_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin_decorator
def delete_group(group_id):
    # Fetch user ID
    user_id = get_jwt_identity()
    
    # Fetch the group from the DB and check ownership
    stmt = db.select(Group).filter_by(id=group_id, created_by=user_id)
    group = db.session.scalar(stmt)

    # If the group does not exist or the user is not the owner, return error msg
    if not group:
        return {"error": "You are not authorised to delete this group."}, 403   

    # If the group exists, delete it and return acknowledgment msg
    db.session.delete(group)
    db.session.commit()
    
    return {"message": f"Group {group.id} has been deleted successfully!"}, 200

