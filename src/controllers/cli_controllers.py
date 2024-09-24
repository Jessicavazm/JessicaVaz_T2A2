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
    # Add users to users table
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
            password = bcrypt.generate_password_hash("123456").decode("utf-8"),
            is_admin = True
        ),
        User(
            name = "User C",
            email = "user_c@email.com",
            password = bcrypt.generate_password_hash("123456").decode("utf-8"),
        )

    ]
    # Add created users to DB
    db.session.add_all(users)
    db.session.commit()
    

    # Add workouts to workouts table
    workouts = [
        Workout(
        title = "Running with friend",
        date = date.today(),
        distance_kms = 10,
        calories_burnt = 235,
        user_id=users[0].id
    ), Workout(
        title = "Running with friend",
        date = date.today(),
        distance_kms = 10,
        calories_burnt = 250,
        user_id=users[1].id
    )]
    # Add created workouts to DB
    db.session.add_all(workouts)
    db.session.commit()


    # Add running groups to groups table
    groups = [
            Group(
                name = "Group A",
                date_created = date.today()
            ), 
            Group(
                name = "Group B",
                date_created = date.today()
            )
        ]
    # Add created groups to DB
    db.session.add_all(groups)
    db.session.commit()


    # Add marathon events to marathons tables
    marathons = [
            Marathon(
                name = "Marathon A",
                date = date(2026, 12, 12), 
                location = "Gold Coast",
                distance_kms = 10
            ), 
            Marathon(
                name = "Marathon B",
                date = date(2025, 10, 8),
                location = "Melbourne",
                distance_kms = 20
            )
        ]
    # Add created marathons to DB and commit changes all changes above to DB
    db.session.add_all(marathons)
    db.session.commit()


    # Add marathon_logs to logs tables
    logs = [
            Log(
                entry_created = date.today(),
                group_id=groups[1].id,  
                marathon_id=marathons[1].id 
            ), 
            Log(
                entry_created = date.today(),
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

