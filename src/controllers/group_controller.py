from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.group import Group,group_schema, groups_schema
from models.user import User
from models.marathon import Marathon
from models.log import Log, log_schema

from utils import auth_as_admin_decorator

# Create workout blueprint
group_bp = Blueprint("group", __name__,url_prefix="/group")


@group_bp.route("/")
def get_all_groups():
    # Create and execute stmt, order by asc order
    # Convert groups to list to use IF statement 
    stmt = db.select(Group).order_by(Group.name.asc())
    groups = list(db.session.scalars(stmt))
    if groups:
        # Serialise data using groups_schema
        return groups_schema.dump(groups), 200
    # Else returns error message
    else:
        return {"Error": "No groups to display."}, 400


# Create route for 'GET' a specific group
@group_bp.route("/<int:group_id>")
def get_a_group(group_id):
    # Use stmt and filter_by to select a specific group
    stmt = db.select(Group).filter_by(id=group_id)
    group = db.session.scalar(stmt)
    # If marathon returns it, Else returns error msg
    if group:
        return group_schema.dump(group)
    else:
        return {"error": f"Group with {group_id} not found."}, 404
    

# Create 'register' group route,'POST' method to insert data into DB
# Auth_as_admin decorator only allows admin to create a group
@group_bp.route("/register", methods=["POST"])
@jwt_required()
@auth_as_admin_decorator
def register_group():
    try:
        # Get the admin using JWT 
        admin_id = get_jwt_identity()
        admin_user = User.query.get(admin_id)  

        # Check if admin already has a group
        if admin_user.group_id:
            return {"error": "You have already created a group."}, 400

        # Get the fields from the request and create a new group
        body_data = group_schema.load(request.get_json())
        group = Group(
            name=body_data.get("name"),
            date_created=date.today()
        )
        
        # Add and commit to the database
        db.session.add(group)
        db.session.commit()

        # Update the user's group_id
        admin_user.group_id = group.id
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
            group.name = body_data.get("name") or group.name
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
    

# Create route for admins to enrol their group in marathons events, JWT required
# POST method to insert data in DB
@group_bp.route("/marathon_signup/<int:marathon_id>", methods=["POST"])
@jwt_required()
@auth_as_admin_decorator
def signup_marathon(marathon_id):
    try:
        # Get the admin using JWT 
        admin_id = get_jwt_identity()
        admin_user = User.query.get(admin_id) 

        # Get the group associated with the admin
        group = Group.query.get(admin_user.group_id)
        if not group:
            return {"error": "Group not found, try creating a group first."}, 404

        # Check if the marathon exists
        marathon = Marathon.query.get(marathon_id)
        if not marathon:
            return {"error": "Marathon not found."}, 404
        
        # Check if the group is already signed up for this marathon
        existing_log = Log.query.filter_by(group_id=group.id, marathon_id=marathon_id).first()
        if existing_log:
            return {"error": "This group is already enrolled in this marathon."}, 400

        # Create the log entry
        log_entry = Log(
            entry_created=date.today(),
            group_id=group.id,
            marathon_id=marathon_id  
        )

        # Add the log entry to the database
        db.session.add(log_entry)
        db.session.commit()

        # Return a success message
        return log_schema.dump(log_entry), 201

    except Exception as e:
        return {"error": str(e)}, 500
