from init import db, ma

from marshmallow import fields
from marshmallow.validate import Regexp


# Define users table 
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    
    # Define relationships, set bidirectional relationship.
    workouts = db.relationship("Workout", back_populates = "user")
    group = db.relationship("Group", back_populates= "user")


# Define User Schema to serialize/ deserialized fields
# Unpack complex data with fields.Nested method
class UserSchema(ma.Schema):
    workouts = fields.List(fields.Nested("WorkoutSchema", exclude=["user"]))
    # group = fields.Nested("GroupSchema", only=["name"])

    class Meta:
        fields = ["id", "name", "email", "password", "is_admin", "workouts"]


# Create schema objects to handle one or multiple items
user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])