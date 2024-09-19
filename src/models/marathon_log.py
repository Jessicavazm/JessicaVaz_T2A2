from init import db, ma
from marshmallow import fields


# Define logs table
class Log(db.Model):
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date) 
    

    # Foreign keys
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    marathon_id = db.Column(db.Integer, db.ForeignKey("marathons.id"), nullable=False)


    # Define bidirectional relationships
    groups = db.relationship("Group", back_populates="logs")
    marathons = db.relationship("Marathon", back_populates="logs")


# Define User Schema to serialize/ deserialized fields
# Unpack complex data with fields.Nested method
class LogSchema(ma.Schema):
    group = fields.Nested("UserSchema", only = ["name", "email"])
    marathon = fields.Nested("MarathonSchema", only = ["name", "date"])
    class Meta:
        fields = ["id", "group", "marathon"]


# Create schema objects to handle one or multiple items
log_schema = LogSchema()
logs_schema = LogSchema(many=True)