from flask import Blueprint
from init import db, bcrypt
from models.user import User


# Create a blueprint
db_commands = Blueprint("db", __name__)


# Create tables command
@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created!")


# Seed tables command
@db_commands.cli.command("seed")
def seed_tables():
    users = [
        User(
            name = "User A",
            email = "admin_a@email.com",
            password = bcrypt.generate_password_hash("123456").decode("utf-8"),
            is_admin = True
        ), 
        User(
            name = "User B",
            email = "user_b@email.com",
            password = bcrypt.generate_password_hash("123456").decode("utf-8")
        )
    ]

    db.session.add_all(users)
    db.session.commit()
    print("Tables seeded!")
 

# Drop tables command
@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped!")

