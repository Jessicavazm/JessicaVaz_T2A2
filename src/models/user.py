from init import db, ma

# Define users table 
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(10), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# Define User Schema to serialize/ deserialized fields
class UserSchema(ma.Schema):
    class Meta:
        fields = ["id", "name", "email", "password", "is_admin"]


# Create schema objects to handle one or multiple items
user_schema = UserSchema(exclude=["password"])

users_schema = UserSchema(many=True, exclude=["password"])
