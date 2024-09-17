from init import db, ma
from marshmallow import fields


# Define workouts table
class Workout(db.Model):
    __name__ = "workouts"

    id = db.Column(db.Integer, primary_key=True),
    date = db.Column(db.Date, nullable=False),
    distance = db.Column(db.Float, nullable=False),
    duration = db.Column(db.Float),
    calories_burnt = db.Column(db.Float)

    
    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


# Define Schema
class WorkoutSchema(ma.Schema):
    # user = fields.Nested("UserSchema", only=["name", "email"])
    class Meta:
        fields = ["id", "date", "distance", "duration", "calories_burnt"]


# Create Objects 
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)