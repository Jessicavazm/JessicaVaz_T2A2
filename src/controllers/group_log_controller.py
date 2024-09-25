from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.user import User
from models.group import Group
from models.group_log import GroupLog  

# Create a blueprint for group enrollment
group_signup_bp = Blueprint("signup", __name__, url_prefix="/groups/signup")

# Route for users to join a group
@group_signup_bp.route("/<int:group_id>", methods=["POST"])
@jwt_required()
def join_group(group_id):
    user_id = get_jwt_identity() 
    user = User.query.get(user_id)

    if not user:
        return {"error": "User not found."}, 404

    group = Group.query.get(group_id)
    if not group:
        return {"error": "Group not found."}, 404

    # Check if the user is already part of the group
    existing_entry = GroupLog.query.filter_by(user_id=user.id, group_id=group.id).first()
    if existing_entry:
        return {"error": "You are already a member of this group."}, 400

    # Create a new entry for the user in the group
    new_entry = GroupLog(user_id=user.id, group_id=group.id)
    db.session.add(new_entry)
    db.session.commit()

    return {"message": f"You have successfully joined group {group.name}."}, 201

# Route for users to leave a group
@group_signup_bp.route("/<int:group_id>", methods=["POST"])
@jwt_required()
def leave_group(group_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return {"error": "User not found."}, 404

    group = Group.query.get(group_id)
    if not group:
        return {"error": "Group not found."}, 404

    # Find the entry in the GroupLog table
    entry = GroupLog.query.filter_by(user_id=user.id, group_id=group.id).first()
    if not entry:
        return {"error": "You are not a member of this group."}, 400

    # Remove the entry
    db.session.delete(entry)
    db.session.commit()

    return {"message": f"You have successfully left group {group.name}."}, 200
