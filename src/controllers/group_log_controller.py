from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.user import User
from models.group import Group
from models.group_log import GroupLog  


# Create a blueprint for group enrollment
group_signup_bp = Blueprint("join", __name__, url_prefix="/<int:group_id>")


# POST method => /groups/<group_id>/join
# Route for regular users to join a specific group
# Admin are only allowed to be part of their created group
@group_signup_bp.route("/join", methods=["POST"])  
@jwt_required()
def join_group(group_id):

    # Fetch user and group info
    user_id = get_jwt_identity() 
    user = User.query.get(user_id)
    group = Group.query.get(group_id) 

    # Error message if user or group not found
    if user is None or group is None:
        if user is None:
            return {"error": "User not found."}, 404
        if group is None:
            return {"error": "Group not found, ensure group exists first."}, 404

    # Error msg if user is part of the group already
    existing_entry = GroupLog.query.filter_by(user_id=user.id, group_id=group.id).first()
    if existing_entry:
        return {"error": "You are already a member of this group."}, 400
    
    # Prevent admins from joining any group
    if user.is_admin:
        return {"error": "Admins are only allowed to be part of their created group."}, 403

    # Create a new entry and add to the junction table
    new_entry = GroupLog(user_id=user.id, group_id=group.id)
    db.session.add(new_entry)
    db.session.commit()

    # return acknowledgment msg
    return {"message": f"{user.name} is officially part of the group named {group.name}."}, 201
    

# DELETE method => /groups/<group_id>/unsubscribe
# Route for regular users to leave a specific group
@group_signup_bp.route("/unsubscribe", methods=["DELETE"]) 
@jwt_required()
def leave_group(group_id):

    # Get user id from token
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    # if not user or group return error msg
    if not user:
        return {"error": "User not found."}, 404

    # Fetch group, return error msg if group not found
    group = Group.query.get(group_id)
    if not group:
        return {"error": "Group not found."}, 404
    
    # Fetch the entry from GroupLog table, if not entry return error msg
    entry = GroupLog.query.filter_by(user_id=user.id, group_id=group.id).first()
    if not entry:
        return {"error": "You are not a member of this group."}, 400
    
    # Prevent admins from leaving their group
    if user.is_admin:
        return {"error": "Whoops! You can not leave your own group."}, 403

    # Remove the entry and return acknowledgment msg
    db.session.delete(entry)
    db.session.commit()

    return {"message": f"You have successfully left the group named {group.name}."}, 200
