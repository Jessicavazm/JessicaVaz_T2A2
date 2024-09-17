from init import db, ma

# Define users table and schema
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class UserSchema(ma.Schema):
    class Meta:
        fields = ["id", "name", "email", "password", "is_admin"]


# Create schema objects to handle single or multiple items
user_schema = UserSchema(exclude=["password"])

users_schema = UserSchema(many=True, exclude=["password"])
