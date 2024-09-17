from init import db, ma
from marshmallow import fields


# Define table
class Marathon_entry(db.Model):
    __name__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    

    # Foreign keys
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    marathon_id = db.Column(db.Integer, db.ForeignKey("marathons.id"), nullable=False)


# Define Schema
class EntrySchema(ma.Schema):
    class Meta:
        fields = ["id"]


# Create Objects 
entry_schema = EntrySchema()
entries_schema = EntrySchema(many=True)