from init import db, ma
from marshmallow import fields


# Define 'groups' table
class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.Date)
    experience_level = db.Column(db.String(50), nullable=False)
    members_capacity = db.Column(db.Integer)
    created_by = db.Column(db.String)

    
    # Foreign key to reference 'users' table
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


    # Define bidirectional relationships with 'users' and 'logs' tables
    user = db.relationship("User", back_populates= "group")
    logs = db.relationship("Log", back_populates= "groups", cascade="all, delete")


# Define Group Schema to serialize/ deserialize fields
# Unpack complex data with fields.Nested method
# Only include 'name' and 'email' from 'users' table and exclude 'group' from 'logs' table to avoid redundant data
class GroupSchema(ma.Schema):
    users = fields.List(fields.Nested("UserSchema", only=["name", "email"]))
    logs = fields.List(fields.Nested("LogSchema", exclude=["group"]))

    class Meta:
        fields = ["id", "name", "date_created", "category_level", "members_capacity", "created_by", "users", "logs"]


# Create schema objects to handle one or multiple items 
group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)