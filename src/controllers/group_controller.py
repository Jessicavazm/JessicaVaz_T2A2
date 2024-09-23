from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from psycopg2 import errorcodes

from init import db
from models.group import Group, GroupSchema, group_schema, groups_schema
from models.user import User
from utils import auth_as_admin_decorator

# Create workout blueprint
group_bp = Blueprint("group", __name__,url_prefix="/group")


@group_bp.route("/")
def get_all_groups():
    # Create and execute stmt, order by asc order
    # Convert groups to list to use IF statement 
    stmt = db.select(Group).order_by(Group.title.asc())
    groups = list(db.session.scalars(stmt))
    if groups:
        # Serialise data using groups_schema
        return groups_schema.dump(groups), 200
    # Else returns error message
    else:
        return {"Error": "No groups to display."}, 400


# Create 'register' group route,'POST' method to insert data into DB
# Auth_as_admin decorator only allows admin to create a group
@group_bp.route("/register", methods=["POST"])
@jwt_required()
@auth_as_admin_decorator
def register_group():
    try:
        # Fetch admin's id
        admin_id = get_jwt_identity()
        existing_user = User.query.get(admin_id)  # Get the user directly

        # Check if the user already has a group
        if existing_user.group_id:
            return {"error": "You have already created a group."}, 400

        # Get the fields from the request
        body_data = group_schema.load(request.get_json())
        
        # Create a new group instance
        group = Group(
            title=body_data.get("title"),
            date_created=date.today()
        )
        
        # Add and commit to the database
        db.session.add(group)
        db.session.commit()

        # Update the user's group_id
        existing_user.group_id = group.id
        db.session.commit()

        # Return acknowledgment message
        return group_schema.dump(group), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 400
    except Exception as e:
        return {"error": str(e)}, 500
    

# Create route for updating group info, "PATCH" to insert data into DB
# @auth_as_admin decorator to ensure only admin can perform this action
@group_bp.route("/<int:group_id>", methods = ["PUT", "PATCH"])
@jwt_required()
@auth_as_admin_decorator
def update_group(group_id):
        # Get the fields from body of the request, partial=True to update partial data
        body_data = group_schema.load(request.get_json(), partial=True)
        stmt = db.select(Group).filter_by(id=group_id)
        group = db.session.scalar(stmt)
        # If group exist, edit required fields, ELSE returns error msg
        if group:
            group.title = body_data.get("title") or group.title
            # Commit changes to DB, return updated group
            db.session.commit()
            return group_schema.dump(group)
        else:
            return {"error": f"Group with id {group_id} has not been found."}, 404


# Create route for deleting group, JWT required
# @auth_as_admin decorator to ensure only admin can perform this action
@group_bp.route("/<int:group_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin_decorator
def delete_group(group_id):
    # Fetch the group from DB with stmt
    stmt = db.select(Group).filter_by(id=group_id)
    group = db.session.scalar(stmt)
    # If group exist delete it, ELSE returns error msg
    if group:    
        db.session.delete(group)
        db.session.commit()
        return {"message": f"Group {group_id} has been deleted successfully!"}, 200
    else:
        return {"error": f"Group {group_id} has been not found."}, 404
    

@group_bp.route("/signup/<int:group_id>", methods=["POST"])
@jwt_required()
def signup_group(group_id):
    try:
        # Fetch user ID from JWT
        user_id = get_jwt_identity() 
        user = User.query.get(user_id)

        # Check if the user is already part of a group
        if user.group_id is not None:
            return {"error": "You are part of a group already."}, 400
        
        # Fetch the group instance
        group = Group.query.get(group_id)
        if not group:
            return {"error": "Group not found."}, 404
        
        # Add the user to the group
        user.group_id = group_id
        db.session.commit()
        return {"message": f"You have been added to group {group_id} successfully."}, 201  
    # Handles errors
    except Exception as e:
        return {"error": str(e)}, 500