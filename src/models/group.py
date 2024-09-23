from init import db, ma
from marshmallow import fields


class Group(db.Model):
    # Name of the table
    __tablename__ = "groups"

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.Date)


    # Define bidirectional relationships with 'users' and 'logs' tables
    users = db.relationship("User", back_populates= "group")
    logs = db.relationship("Log", back_populates= "group", cascade="all, delete")


# Define 'group' schema and class 'Meta' fields to serialize/ deserialize data
# Unpack complex data with fields.Nested method
# Only include 'name' and 'email' from 'users' table and exclude 'group' from 'logs' table to avoid redundant data
class GroupSchema(ma.Schema):
    users = fields.List(fields.Nested("UserSchema", only=["name", "email"]))
    logs = fields.List(fields.Nested("LogSchema", exclude=["group"]))
    class Meta:
        fields = ["id", "title", "date_created", "users", "logs"]


# Create schema objects to handle one or multiple items 
group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)