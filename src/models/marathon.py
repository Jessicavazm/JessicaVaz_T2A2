from init import db, ma
from marshmallow import fields


# Define 'marathons' table
class Marathon(db.Model):
    __tablename__ = "marathons"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    distance_kms = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250))


    # Define bidirectional relationships with 'logs' table
    logs = db.relationship("Log", back_populates="marathons", cascade="all, delete")


# Define 'marathons' schema to serialize/ deserialize fields
# Unpack complex data with fields.Nested method
# Only include attribute 'id' from 'logs' table to avoid redundant data
class MarathonSchema(ma.Schema):
    logs = fields.List(fields.Nested("LogSchema", only=["id"]))
    class Meta:
        fields = ["id", "name", "date", "city", "distance_kms", "description", "logs"]


# Create schema objects to handle one or multiple items
marathon_schema = MarathonSchema()
marathons_schema = MarathonSchema(many=True)