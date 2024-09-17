from init import db, ma
from marshmallow import fields


# Define table
class Marathon(db.Model):
    __tablename__ = "marathons"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    distance = db.Column(db.Integer, nullable=False)


    # Define relationship
    groups = db.relationship("Group", back_populates= "marathons")
    entries = db.relationship("MarathonEntry", back_populates="marathons")


# Define Schema
class MarathonSchema(ma.Schema):
    groups = fields.List(fields.Nested("GroupSchema", only=["name"]))
    entries = fields.List(fields.Nested("EntrySchema", only=["id"]))

    class Meta:
        fields = ["id", "description", "date", "location", "distance", "groups", "id"]


# Create Objects 
marathon_schema = MarathonSchema()
marathons_schema = MarathonSchema(many=True)