from init import db, ma
from marshmallow import fields


# Define 'logs' table
class Log(db.Model):
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date) 
    

    # Foreign keys to reference both 'groups' and 'marathons' tables
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    marathon_id = db.Column(db.Integer, db.ForeignKey("marathons.id"), nullable=False)


    # Define bidirectional relationships with 'groups' and 'marathons' tables
    groups = db.relationship("Group", back_populates="logs")
    marathons = db.relationship("Marathon", back_populates="logs")


# Define 'log' schema to serialize/ deserialize fields
# Unpack complex data with fields.Nested method
# Only include attribute 'name' from 'groups' table and 'name' and 'date' from marathons table
class LogSchema(ma.Schema):
    groups = fields.List(fields.Nested("GroupSchema", only = ["name"]))
    marathons = fields.List(fields.Nested("MarathonSchema", only = ["name", "date"]))
    class Meta:
        fields = ["id", "groups", "marathons"]


# Create schema objects to handle one or multiple items
log_schema = LogSchema()
logs_schema = LogSchema(many=True)