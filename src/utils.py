# Import functools to use wraps method
import functools

from flask_jwt_extended import get_jwt_identity

from init import db
from models.user import User

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
        if user.is_admin:
            return fn(*args, **kwargs)
        # Else return error message
        else:
            return {"error": "Only admin can perform this action"}, 403
    
    return wrapper