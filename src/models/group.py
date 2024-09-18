from init import db, ma
from marshmallow import fields


# Define table
class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.Date)
    experience_level = db.Column(db.String(50), nullable=False)
    members_capacity = db.Column(db.Integer)
    created_by = db.Column(db.String)

    
    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


    # Define relationship
    user = db.relationship("User", back_populates= "group")
    # marathon = db.relationship("Marathon", back_populates= "groups")


# Define Schema
class GroupSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name", "email"])
    # marathon = fields.List(fields.Nested("MarathonSchema", exclude=["group"]))


    class Meta:
        fields = ["id", "name", "date_created", "category_level", "members_capacity", "created_by", "user"]


# Create Objects 
group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)