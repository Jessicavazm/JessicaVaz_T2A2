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
    # FK to reference the groups table
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))

    
    # Define bidirectional relationships with 'workouts' and 'groups' tables.
    workouts = db.relationship("Workout", back_populates = "user", cascade="all, delete")
    group = db.relationship("Group", back_populates= "users", cascade="all, delete")


# Define 'user' schema and class 'Meta' fields to serialize/ deserialize data
# Unpack complex data with fields.Nested method
# Exclude 'user' from 'workouts' table, and only add 'title' from 'groups' table to avoid redundant data
class UserSchema(ma.Schema):
    workouts = fields.List(fields.Nested("WorkoutSchema", exclude=["user"]))
    group = fields.Nested("GroupSchema", only=["title"])
    class Meta:
        fields = ["id", "name", "email", "password", "is_admin", "workouts", "group"]


# Create schema objects to handle one or multiple items
user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])