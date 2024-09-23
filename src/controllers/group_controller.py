from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from psycopg2 import errorcodes

from init import db
from models.group import Group, GroupSchema, group_schema, groups_schema
from utils import auth_as_admin_decorator

# Create workout blueprint
group_bp = Blueprint("group", __name__,url_prefix="/group")


# Create route for see all groups, 'GET' method
@group_bp.route("/")
def get_all_groups():
    try:    
        # Create and execute stmt, order by ascending title
        stmt = db.select(Group.title, Group.members_capacity, Group.created_by).order_by(Group.title.asc())
        groups = db.session.execute(stmt).all()
        # Check if groups exist, display title and group's capacity, Else returns error msg
        if groups:
            return [{"title": group.title, "Members capacity": group.members_capacity, "Created_by": group.created_by} for group in groups], 200
        else:
            return {"Error": "No groups created."}, 400
    except SQLAlchemyError as e:
        return {"Error": str(e)}, 500


# Create 'register' group route,'POST' method to insert data into DB
# Auth_as_admin decorator only allows admin to create a group
@group_bp.route("/register", methods=["POST"])
@jwt_required()
@auth_as_admin_decorator
def register_group():
    try:
        # Fetch admin's id and ensure they haven't created a group yet
        admin_id = get_jwt_identity()
        existing_group = Group.query.filter_by(user_id=admin_id)
        if existing_group:
            return {"error": "You have created a group already."}, 400
        # Get the fields from the body of the request, deserialize using group_schema
        body_data = group_schema.load(request.get_json())
        # Create a new group instance
        group = Group(
            title=body_data.get("title"),
            date_created=date.today(),
            members_capacity=body_data.get("members_capacity"),
            created_by=body_data.get("created_by"),
            user_id=admin_id
        )
        # Add and commit to the DB
        db.session.add(group)
        db.session.commit()
        # Return acknowledgment message
        return group_schema.dump(group), 201
    # Return not null violation personalised message   
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return{"error": f"The column {err.orig.diag.column_name} is required"}, 400
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
            group.members_capacity = body_data.get("members_capacity") or group.members_capacity
            # Commit changes to DB, return updated workout
            db.session.commit()
            return group_schema.dump(group)
        else:
            return {"error": f"Workout with id {group_id} has not been found."}, 404


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
        return {"message": f"group {group_id} has been deleted successfully!"}, 200
    else:
        return {"error": f"Workout {group_id} has been not found."}, 404