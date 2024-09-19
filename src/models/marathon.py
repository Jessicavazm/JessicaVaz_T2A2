from init import db, ma
from marshmallow import fields


# Define marathons table
class Marathon(db.Model):
    __tablename__ = "marathons"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    distance_kms = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250))


    # Define bidirectional relationships
    logs = db.relationship("Log", back_populates="marathons", cascade="all, delete")


# Define User Schema to serialize/ deserialized fields
# Unpack complex data with fields.Nested method
class MarathonSchema(ma.Schema):
    log = fields.List(fields.Nested("LogSchema", only=["id"]))
    class Meta:
        fields = ["id", "name", "date", "city", "distance_kms", "description", "log"]


# Create schema objects to handle one or multiple items
marathon_schema = MarathonSchema()
marathons_schema = MarathonSchema(many=True)