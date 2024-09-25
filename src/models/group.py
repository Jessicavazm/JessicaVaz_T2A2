from datetime import date
from init import db, ma
from marshmallow import fields


class Group(db.Model):
    # Name of the table
    __tablename__ = "groups"

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.Date, default=date.today)

    # Define bidirectional relationships with groups_logs and marathons_logs
    # Cascade to delete logs if group is deleted
    group_logs = db.relationship("GroupLog", back_populates= "group", cascade="all, delete")
    marathon_logs = db.relationship("MarathonLog", back_populates= "group", cascade="all, delete")


# Define 'group' schema and class 'Meta' fields to serialize/ deserialize data
# Unpack complex data with fields.Nested method, fields.List used for a list of logs
# Exclude 'group' from log and group schemas to avoid redundant data
class GroupSchema(ma.Schema):
    group_logs = fields.List(fields.Nested("GroupLogSchema", exclude=["group"]))
    marathon_logs = fields.List(fields.Nested("LogSchema", exclude=["group"]))
    class Meta:
        fields = ["id", "name", "date_created", "logs", "group_logs"]
        ordered = True


# Create schema objects to handle one or multiple items 
group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)