from datetime import date

from flask import Blueprint

from init import db, bcrypt
from models.user import User
from models.workout import Workout
from models.group import Group
from models.marathon import Marathon
from models.log import Log


# Create db_commands blueprint
db_commands = Blueprint("db", __name__)


# Command to create tables
@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created!")


# Command to seed the tables
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
    # Add created users to DB
    db.session.add_all(users)
    

    workouts = [
        Workout(
        title = "Running with friend",
        date = date.today(),
        distance_kms = 10,
        calories_burnt = 235,
        user = users[0]
    ), Workout(
        title = "Running with friend",
        date = date.today(),
        distance_kms = 10,
        calories_burnt = 250,
        user = users[1]
    )]
    # Add created workouts to DB
    db.session.add_all(workouts)


    groups = [
            Group(
                title = "Group A",
                date_created = date.today(),
                members_capacity = 5,
                created_by = "Jess",
                user = users[1]
            ), 
            Group(
                title = "Group B",
                date_created = date.today(),
                members_capacity = 3,
                created_by = "Iryna",
                user = users[0]
            )
        ]
    # Add created groups to DB
    db.session.add_all(groups)


    marathons = [
            Marathon(
                name = "Marathon A",
                date = date.today(), 
                city = "Gold Coast",
                distance_kms = 10,
                description = "Marathon for all levels"
            ), 
            Marathon(
                name = "Marathon B",
                date = date.today(),
                city = "Melbourne",
                distance_kms = 20,
                description = "Marathon for advanced level"
            )
        ]
    # Add created marathons to DB and commit changes all changes above to DB
    db.session.add_all(marathons)
    db.session.commit()


    logs = [
            Log(
                date = date.today(),
                group_id=groups[1].id,  
                marathon_id=marathons[1].id 
            ), 
            Log(
                date = date.today(),
                group_id=groups[0].id,  
                marathon_id=marathons[0].id 
            )
        ]
    # Add created logs and commit changes to DB
    db.session.add_all(logs)
    db.session.commit()
    print("Tables seeded!")


# Command to drop the tables
@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped!")

