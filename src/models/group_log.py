from datetime import date

from init import db, ma
from marshmallow import fields


class GroupLog(db.Model):
    __tablename__ = "group_logs"

    id = db.Column(db.Integer, primary_key=True)
    entry_created = db.Column(db.Date) 
    
    # Foreign keys to reference both 'users' and 'groups' tables
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)

    # Define bidirectional relationships with 'users' and 'groups' tables
    user = db.relationship("User", back_populates="group_logs")
    group = db.relationship("Group", back_populates="group_logs")


# Define 'group_log' schema and class 'Meta' fields to serialize/ deserialize data
# Unpack complex data with fields.Nested method
# Exclude group_logs from user and group schema to avoid redundant data info
class GroupLogSchema(ma.Schema):
    user = fields.Nested("UserSchema", exclude=["group_logs"])
    group = fields.Nested("GroupSchema", exclude=["group_logs"])
    class Meta:
        fields = ["id", "entry_created", "user", "group"]
        ordered = True


# Create schema objects to handle one or multiple items
group_log_schema = GroupLogSchema()
group_logs_schema = GroupLogSchema(many=True)