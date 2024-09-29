from datetime import date

from marshmallow import fields
from marshmallow.validate import OneOf

from init import db, ma


# Specific entries allowed for workout title attribute
VALID_STATUSES = ("Treadmill", "Outside run", "Outside walk", "Marathon run")

class Workout(db.Model):
    # Name of the table
    __tablename__ = "workouts"

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date =db.Column(db.Date, default=date.today)
    distance_kms = db.Column(db.Integer, nullable=False)
    calories_burnt = db.Column(db.Integer)

    # Define FK to reference 'users' table
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Define bidirectional relationships with 'users' table
    user = db.relationship("User", back_populates = "workouts")


# Define 'workout' schema and class 'Meta' fields to serialize/ deserialize data
# Unpack complex data with fields.Nested method
# Only include attribute 'name' from 'users' table to avoid redundant data
class WorkoutSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["id", "name"])

    # Title validation using a constant
    title = fields.String(required=True, validate=OneOf(VALID_STATUSES))
    
    class Meta:
        fields = ["id", "title", "date", "distance_kms", "calories_burnt", "user"]
        ordered = True


# Create schema objects to handle one or multiple items
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)