from init import db, ma

from marshmallow import fields
from marshmallow.validate import Regexp


class User(db.Model):
    # Name of the table
    __tablename__ = "users"

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    

    # Define bidirectional relationships with 'workouts' and 'groups' tables
    # Cascade to delete workouts and group if user is deleted
    workouts = db.relationship("Workout", back_populates = "user", cascade="all, delete")
    group_logs = db.relationship("GroupLog", back_populates="user", cascade="all, delete")

# Define 'user' schema and class 'Meta' fields to serialize/ deserialize data
# Unpack complex data with fields.Nested method, fields.List to unpack a list of objects
# Exclude 'user' from workouts and group_logs schemas to avoid redundant data
class UserSchema(ma.Schema):
    workouts = fields.List(fields.Nested("WorkoutSchema", exclude=["user"]))
    group_logs = fields.List(fields.Nested("GroupLogSchema", exclude=["user"]))
    class Meta:
        fields = ["id", "name", "email", "password", "is_admin", "workouts", "group_logs"]
        ordered = True 


# Create schema objects to handle one or multiple items
user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])