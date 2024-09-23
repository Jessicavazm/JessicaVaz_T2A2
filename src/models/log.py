from init import db, ma
from marshmallow import fields


class Log(db.Model):
    # Name of the table
    __tablename__ = "logs"

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date) 
    

    # Foreign keys to reference both 'groups' and 'marathons' tables
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    marathon_id = db.Column(db.Integer, db.ForeignKey("marathons.id"), nullable=False)


    # Define bidirectional relationships with 'groups' and 'marathons' tables
    group = db.relationship("Group", back_populates="logs")
    marathon = db.relationship("Marathon", back_populates="logs")

# Define 'log' schema and class 'Meta' fields to serialize/ deserialize data
# Unpack complex data with fields.Nested method
# Only include attribute 'name' from 'groups' table and 'name' and 'date' from marathons table
class LogSchema(ma.Schema):
    group = (fields.Nested("GroupSchema", only = ["title"]))
    marathon = (fields.Nested("MarathonSchema", only = ["name", "date"]))
    class Meta:
        fields = ["id", "group", "marathon"]


# Create schema objects to handle one or multiple items
log_schema = LogSchema()
logs_schema = LogSchema(many=True)