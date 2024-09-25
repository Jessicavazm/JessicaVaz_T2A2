from datetime import date

from init import db, ma
from marshmallow import fields


class MarathonLog(db.Model):
    # Name of the table
    __tablename__ = "marathon_logs"

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    entry_created = db.Column(db.Date, default=date.today) 
    
    # Foreign keys to reference both 'groups' and 'marathons' tables
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    marathon_id = db.Column(db.Integer, db.ForeignKey("marathons.id"), nullable=False)

    # Define bidirectional relationships with 'groups' and 'marathons' tables
    group = db.relationship("Group", back_populates="marathon_logs")
    marathon = db.relationship("Marathon", back_populates="marathon_logs")


# Define 'log' schema and class 'Meta' fields to serialize/ deserialize data
# Unpack complex data with fields.Nested method
# Only include attribute 'name' from 'groups' table
# Exclude logs from marathon schema to avoid redundant data info
class MarathonLogSchema(ma.Schema):
    group = fields.Nested("GroupSchema", only =["marathon_logs"])
    marathon = fields.Nested("MarathonSchema", exclude=["marathon_logs"])
    class Meta:
        fields = ["id", "entry_created", "group", "marathon"]
        ordered = True


# Create schema objects to handle one or multiple items
marathon_log_schema = MarathonLogSchema()
marathon_logs_schema = MarathonLogSchema(many=True)