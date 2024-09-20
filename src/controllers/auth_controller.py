from datetime import timedelta

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from models.user import User, user_schema, UserSchema
from init import db, bcrypt

from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes


# Create authorisation blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# Create 'register' route, use "POST" since data will be inserted to DB
@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:    
        # Get the data from the body of the request and stores it in variable = body_data
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
        # Display personalised messages in case of data violations
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return{"error": f"The column {err.orig.diag.column_name} is required"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address must be unique"}, 400


# Create 'login' route
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
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=2))
        return{"email": user.email, "token": token}
    # else return error message
    else:
        return {"error": "Invalid credentials"}, 400


# Update user's details, token required
@auth_bp.route("users/<int:user_id>", methods = ["PUT", "PATCH"])
@jwt_required()
def update_user(user_id):
    # Get the fields from body of the request, partial=True to update partial data
    body_data = UserSchema().load(request.get_json(), partial=True)
    password = body_data.get("password")
    # Fetch user from DB using stmt, user.id comes from token, enforces authorisation
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)
    # If the user exist, update the required fields
    if user:
        # 'OR' statement evaluates what comes true first
        user.name = body_data.get("name") or user.name
        user.email = body_data.get("email") or user.email
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        # Commit to the DB
        db.session.commit()
        # Return an acknowledgement message
        return user_schema.dump(user)
    # Else return error message
    else:
        return {"error": "User does not exist."}, 400


# Delete user route, token required
@auth_bp.route("users/<int:user_id>", methods=["DELETE"])
@jwt_required()
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


