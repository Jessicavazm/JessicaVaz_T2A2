from init import db, ma
from marshmallow import fields


# Define workouts table
class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Float)
    calories_burnt = db.Column(db.Integer)

    
    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


    # Define relationship
    user = db.relationship("User", back_populates = "workouts")


# Define Schema
class WorkoutSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name", "email"])
    class Meta:
        fields = ["id", "date", "distance", "duration", "calories_burnt", "user"]


# Create Objects 
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)