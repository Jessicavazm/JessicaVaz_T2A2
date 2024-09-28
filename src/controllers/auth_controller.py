from datetime import timedelta

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db, bcrypt
from models.user import User, UserSchema, user_schema


# Authorisation blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# GET method => /auth/register
# Route for user to register in app
@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:    
        # Get the data from the body of the request, including password
        body_data = UserSchema().load(request.get_json())
        
        # Create an instance of User model, lower to ensure unique email 
        user = User(
            name = body_data.get("name"),
            email = body_data.get("email").lower()
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
    # Display personalised msgs for data violations
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return{"error": f"The column {err.orig.diag.column_name} is required"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address must be unique"}, 400
    except Exception as e:
        return {"error": f"An unexpected error has occurred {e}"}


# POST method = auth/login
# Route for user to login in
@auth_bp.route("/login", methods = ["POST"])
def login_user():
    # Get data from request body
    body_data = request.get_json()

    # If not returns error msg for missing field 
    if not body_data.get("email") or not body_data.get("password"):
        return {"error": "Email and password are required."}, 400
    
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


# PUT, PATCH method => /auth/users/<user_id>
# Route for users to update their info
@auth_bp.route("/users/", methods = ["PUT", "PATCH"])
@jwt_required()
def update_user():
    try:    
        # Get the fields from body of the request, partial=True to update partial data
        body_data = UserSchema().load(request.get_json(), partial=True)
        password = body_data.get("password")
        # Fetch user from DB using stmt and token
        stmt = db.select(User).filter_by(id=get_jwt_identity())
        user = db.session.scalar(stmt)
        
        # If the user exist, update the required fields
        if user:
            if body_data.get("name") is not None:  
                user.name = body_data["name"]
            if body_data.get("email") is not None:  
                user.email = body_data["email"].lower()
            if password is not None:
                user.password = bcrypt.generate_password_hash(password).decode("utf-8") 
                
            # Commit to the DB
            db.session.commit()
            # Return an acknowledgement msg
            return user_schema.dump(user)
        else:
        # Else returns error msg
            return {"error": "User does not exist."}, 400
    # Display error msgs
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address must be unique"}, 400
    # Catches general errors and display info
    except Exception as e:
        return {"error": f"An unexpected error has occurred {e}"}


# DELETE method => /auth/users/<user_id>
# Route for deleting users, both admin and the actual user can perform this function
@auth_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    try:
        # Get the current user's identity from the JWT 
        current_user_id = get_jwt_identity()

        # Find the user to be deleted in DB
        user_to_delete = User.query.get(user_id)

        # If no requested user to delete return error msg
        if not user_to_delete:
            return {"error": f"User with ID {user_id} does not exist."}, 404

        # Find the current user in the DB
        current_user = User.query.get(current_user_id)

        # If the user making the request is not found, return error msg
        if not current_user:
            return {"error": "Current user not found, please check your credentials."}, 404

        # Check if the current user is either the user themselves or an admin user
        print(f"Current User ID: {current_user.id}, Is Admin: {current_user.is_admin}")
        if current_user.id == user_id or current_user.is_admin:
            # Delete the user
            db.session.delete(user_to_delete)
            db.session.commit()
            return {"message": f"{user_to_delete.name} with ID number {user_id} has been successfully deleted."}, 200
        else:
            # Return not authorised msg
            return {"error": "Whoops! You don't have permission to delete this user."}, 403
    except Exception as e:
        return {"error": "An unexpected error occurred.", "details": str(e)}, 500
