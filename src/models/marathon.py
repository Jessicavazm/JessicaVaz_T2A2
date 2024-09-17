from init import db, ma
from marshmallow import fields


# Define table
class Marathon(db.Model):
    __name__ = "marathons"

    id = db.Column(db.Integer, primary_key=True),
    name = db.Column(db.String(50), nullable=False),
    description = db.Column(db.String(250)),
    date = db.Column(db.Date, nullable=False),
    time = db.Column(db.Time, nullable=False),
    location = db.Column(db.String(100), nullable=False),
    distance = db.Column(db.Integer, nullable=False)


# Define Schema
class MarathonSchema(ma.Schema):
    # user = fields.Nested("UserSchema", only=["name", "email"])
    class Meta:
        fields = ["id", "description", "date", "location", "distance"]


# Create Objects 
marathon_schema = MarathonSchema()
marathons_schema = MarathonSchema(many=True)