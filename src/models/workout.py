from init import db, ma
from marshmallow import fields


# Define 'workouts' table
class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    distance_kms = db.Column(db.Integer, nullable=False)
    duration_minutes = db.Column(db.Integer)
    calories_burnt = db.Column(db.Integer)

    
    # Define FK to reference 'users' table
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


    # Define bidirectional relationships with 'users' table
    user = db.relationship("User", back_populates = "workouts")


# Define 'workout' schema to serialize/ deserialize fields
# Unpack complex data with fields.Nested method
# Only include attribute 'name' from 'users' table to avoid redundant data
class WorkoutSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name"])
    
    class Meta:
        fields = ["id", "date", "distance_kms", "duration_minutes", "calories_burnt", "user"]


# Create schema objects to handle one or multiple items
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)