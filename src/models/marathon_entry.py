from init import db, ma
from marshmallow import fields


# Define table
class MarathonEntry(db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date) 
    

    # Foreign keys
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    marathon_id = db.Column(db.Integer, db.ForeignKey("marathons.id"), nullable=False)


    # Define relationship
    # group = db.relationship("Group", back_populates="entries")
    # marathon = db.relationship("Marathon", back_populates="entries")


# Define Schema
class EntrySchema(ma.Schema):
    # group = fields.Nested("UserSchema", only = ["name", "email"])
    # marathon = fields.Nested("MarathonSchema", only = ["name", "date"])

    class Meta:
        fields = ["id"]


# Create Objects 
entry_schema = EntrySchema()
entries_schema = EntrySchema(many=True)