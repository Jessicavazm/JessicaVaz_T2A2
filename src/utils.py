# Import functools to use wraps method
import functools

from flask_jwt_extended import get_jwt_identity, jwt_required

from init import db
from models.user import User
from models.group import Group
from models.group_log import GroupLog


# Create an admin decorator
# Implement the function inside of the decorator
# Decorator and wraps method takes the 'function' parameter
def auth_as_admin_decorator(fn):
    @functools.wraps(fn)
    # *args and *kwargs to accept different types of arguments 
    def wrapper(*args, **kwargs):
        # Get user id with get_jwt_identity
        user_id = get_jwt_identity()
        # fetch user from DB using stmt
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        
        # IF user is admin execute the function that called this decorator
        if user and user.is_admin:
            return fn(*args, **kwargs)
        # Else return error message
        else:
            return {"error": "Only admin can perform this action"}, 403
    return wrapper


def admin_group_check_decorator(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # Get user id with get_jwt_identity
        user_id = get_jwt_identity()  
        # Check if the user is an admin
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)

        # Returns error msg
        if user is None or not user.is_admin:
            return {"error": "Admin access required to create a group."}, 403

        # Check if the admin has already created a group through group log table
        existing_group = Group.query.filter_by(created_by=user_id).first()
        if existing_group:
            return {"error": "Admin can only create one group."}, 403

        # Execute the function
        return fn(*args, **kwargs)
    return wrapper
