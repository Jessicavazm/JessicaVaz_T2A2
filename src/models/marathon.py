from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

from init import db, ma


class Marathon(db.Model):
    # Name of the table
    __tablename__ = "marathons"

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    distance_kms = db.Column(db.Integer, nullable=False)
    
    # Define bidirectional relationships with 'logs' table
    # Cascade to delete logs and group if marathon is deleted
    marathon_logs = db.relationship("MarathonLog", back_populates="marathon", cascade="all, delete")

# Define 'marathon' schema and class 'Meta' fields to serialize/ deserialize data
# Unpack complex data with fields.Nested method, fields.List to unpack a list of logs
# Exclude marathon from log schema to avoid redundant data info
class MarathonSchema(ma.Schema):
    marathon_logs = fields.List(fields.Nested("MarathonLogSchema", only=["id", "entry_created"]))
    
    # Validation for 'name'. Name containing two names is allowed eg: 'Coder academy'
    name = fields.String(required=True, validate=And(Length(min=4, max=30, error="Name must be between 4 and 30 characters in length."), Regexp("^[A-Z][a-zA-Z]*( [A-Z][a-zA-Z]*)*$", error="Name must start with an uppercase letter and contain only letters.")))
    
    # Validation for attribute 'location'
    # Allows letter, numbers, spaces, apostrophes and commas eg: Location: 12 O'Connor st, Melbourne
    location = fields.String(required=True, validate=And(Length(min=10, max=50, error="Location must be between 10 and 50 characters in length."), Regexp(r"^(?=(.*[a-zA-Z]){2,})(?!.*([', ])\2)[a-zA-Z0-9]+(?:[', ]+[a-zA-Z0-9]+)*$", error="Location must contain letters and may include numbers, spaces, apostrophes, and commas. Consecutive apostrophes, commas and spaces are not allowed.")))


    class Meta:
        fields = ["id", "name", "event_date", "location", "distance_kms", "marathon_logs"]
        ordered = True


# Create schema objects to handle one or multiple items
marathon_schema = MarathonSchema()
marathons_schema = MarathonSchema(many=True)