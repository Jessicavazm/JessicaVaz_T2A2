from init import db, ma
from marshmallow import fields


# Define table
class Group(db.Model):
    __name__ = "groups"

    id = db.Column(db.Integer, primary_key=True),
    name = db.Column(db.String(50)),
    date_created = db.Column(db.Date, nullable=False),
    category_level = db.Column(db.String(50), nullable=False),
    members_capacity = db.Column(db.Integer),
    created_by = db.Column(db.String)

    
    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


# Define Schema
class GroupSchema(ma.Schema):
    # user = fields.Nested("UserSchema", only=["name", "email"])
    class Meta:
        fields = ["id", "name", "date_created", "category_level", "members_capacity", "created_by"]


# Create Objects 
group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)