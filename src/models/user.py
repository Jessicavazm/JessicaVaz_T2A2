from init import db, ma

from marshmallow import fields
from marshmallow.validate import Length, And, Regexp


class User(db.Model):
    # Name of the table
    __tablename__ = "users"

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
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


    # User name validation, name containing two names is allowed eg: 'Coder academy'
    name = fields.String(required=True, validate=And(Length(min=2, max=20, error="Name must be between 2 and 20 characters in length."), Regexp("^[A-Z][a-zA-Z]*( [A-Z][a-zA-Z]*)*$", error="Name must start with an uppercase letter and contain only letters.")))

    # User email validation
    email = fields.String(required=True, validate=And(Length(min=5, max=50, error="Email must be between 5 and 50 characters in length."), Regexp("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", error="Invalid email format: The email cannot have consecutive dots, must have a local part, a non-empty domain name and a top-level domain containing at least two letters. Valid characters includes letters, numbers, underscore, period, percent sign, plus sign and hyphen.")))

    # User password validation
    password = fields.String(required=True, validate=And(Length(min=6, max=20, error="Password must be a minimum of 6 characters and maximum of 20 characters."), Regexp(r"^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?])[A-Za-z\d!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]{6,}$", error="Invalid password format. Password must contain one upper case letter, one digit and one special character.")))


    class Meta:
        fields = ["id", "name", "email", "password", "is_admin", "workouts", "group_logs"]
        ordered = True 


# Create schema objects to handle one or multiple items
user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])