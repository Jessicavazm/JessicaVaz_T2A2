from datetime import date
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

from init import db, ma


class Group(db.Model):
    # Name of the table
    __tablename__ = "groups"

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.Date, default=date.today)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

    # Define bidirectional relationships with group_admin creator, groups_logs and marathons_logs
    # Cascade to delete logs if group is deleted
    group_admin = db.relationship("User", back_populates= "group_created", cascade="all, delete")
    group_logs = db.relationship("GroupLog", back_populates= "group", cascade="all, delete")
    marathon_logs = db.relationship("MarathonLog", back_populates= "group", cascade="all, delete")


# Define 'group' schema and class 'Meta' fields to serialize/ deserialize data
# Unpack complex data with fields.Nested method, fields.List used for a list of logs
# Exclude 'group' from log and group schemas to avoid redundant data
class GroupSchema(ma.Schema):
    group_admin = fields.Nested("UserSchema", only=["name"]) 
    group_logs = fields.List(fields.Nested("GroupLogSchema", exclude=["group"]))
    marathon_logs = fields.List(fields.Nested("MarathonLogSchema", exclude=["group"]))

    # Validation for attribute 'name', 
    # Name containing two names is allowed eg: 'Coder academy'
    name = fields.String(required=True, validate=And(Length(min=4, max=20, error="Name must be between 4 and 20 characters in length."), Regexp("^[A-Z][a-zA-Z]*( [A-Z][a-zA-Z]*)*$", error="Name must start with an uppercase letter and contain only letters.")))

    class Meta:
        fields = ["id", "name", "date_created", "created_by", "group_admin", "group_logs", "marathon_logs"]
        ordered = True


# Create schema objects to handle one or multiple items 
group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)