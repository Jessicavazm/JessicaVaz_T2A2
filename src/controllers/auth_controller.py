from datetime import timedelta

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db, bcrypt

from models.user import User, UserSchema, user_schema
from models.group import Group
from utils import auth_as_admin_decorator


# Authorisation blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# Route for user to register in app
@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:    
        # Get the data from the body of the request
        body_data = UserSchema().load(request.get_json())
        # Create an instance of User model
        user = User(
            name = body_data.get("name"),
            email = body_data.get("email")
        )
        # If user provides password, hash it
        password = body_data.get("password")
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        # Add and commit to DB
        db.session.add(user)
        db.session.commit()
        # Return acknowledgment and status code
        return user_schema.dump(user), 201
    except IntegrityError as err:
        # Display personalised msgs for data violations
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return{"error": f"The column {err.orig.diag.column_name} is required"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address must be unique"}, 400


# Route for user to login in
@auth_bp.route("/login", methods = ["POST"])
def login_user():
    # Get data from request body
    body_data = request.get_json()
    # Stmt to find user in DB with that specific email
    stmt = db.select(User).filter_by(email=body_data["email"])
    user = db.session.scalar(stmt)
    # If user exist and password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        # Create token and return it to user
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return{"email": user.email, "token": token}
    # else return error msg
    else:
        return {"error": "Invalid credentials"}, 400


# Route for users to update their info
@auth_bp.route("users/<int:user_id>", methods = ["PUT", "PATCH"])
@jwt_required()
def update_user(user_id):
    # Get the fields from body of the request, partial=True to update partial data
    body_data = UserSchema().load(request.get_json(), partial=True)
    password = body_data.get("password")
    # Fetch user from DB using stmt and token
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)
    # If the user exist, update the required fields
    if user:
        # 'OR' statement evaluates what comes true first and execute it
        user.name = body_data.get("name") or user.name
        user.email = body_data.get("email") or user.email
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        # Commit to the DB
        db.session.commit()
        # Return an acknowledgement msg
        return user_schema.dump(user)
    # Else returns error msg
    else:
        return {"error": "User does not exist."}, 400


# Route for deleting users, admin or user can perform this (add user to this, unfinished)
@auth_bp.route("users/<int:user_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin_decorator
def delete_user(user_id):
    # Find user in DB using stmt
    stmt = db.select(User).filter_by(id= user_id)
    user = db.session.scalar(stmt)
    # If user exist, delete user and commit changes to DB
    # Return acknowledgement message
    if user:
        db.session.delete(user)
        db.session.commit()
        return {"message": f"User with {user_id} has been successfully deleted."}
    # Else returns error message
    else:
        return {"message": f"User with id {user_id} has not been found."}