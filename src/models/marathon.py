from init import db, ma
from marshmallow import fields


class Marathon(db.Model):
    # Name of the table
    __tablename__ = "marathons"

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    distance_kms = db.Column(db.Integer, nullable=False)


    # Define bidirectional relationships with 'logs' table
    logs = db.relationship("Log", back_populates="marathon", cascade="all, delete")

# Define 'marathon' schema and class 'Meta' fields to serialize/ deserialize data
# Unpack complex data with fields.Nested method
# Only include attribute 'id' from 'logs' table to avoid redundant data
class MarathonSchema(ma.Schema):
    logs = fields.List(fields.Nested("LogSchema", only=["id", "entry_created"]))
    class Meta:
        fields = ["id", "name", "date", "location", "distance_kms", "logs"]


# Create schema objects to handle one or multiple items
marathon_schema = MarathonSchema()
marathons_schema = MarathonSchema(many=True)