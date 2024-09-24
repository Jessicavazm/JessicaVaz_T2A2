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


    # Add users to users table
    users = [
        User(
            name = "User A",
            email = "admin_a@email.com",
            password = bcrypt.generate_password_hash("123456").decode("utf-8"),
            is_admin = True,
            group=groups[0]
        ), 
        User(
            name = "User B",
            email = "user_b@email.com",
            password = bcrypt.generate_password_hash("123456").decode("utf-8"),
            is_admin = True,
            group=groups[0]

        ),
        User(
            name = "User C",
            email = "user_c@email.com",
            password = bcrypt.generate_password_hash("123456").decode("utf-8"),
            group=groups[1]

        )
    ]
    # Add created users to DB
    db.session.add_all(users)


    # Add workouts to workouts table
    workouts = [
        Workout(
        title = "Running with friend",
        date = date.today(),
        distance_kms = 10,
        calories_burnt = 235,
        user=users[0]
    ), Workout(
        title = "Running with friend",
        date = date.today(),
        distance_kms = 10,
        calories_burnt = 250,
        user=users[1]
    )]
    # Add created workouts to DB
    db.session.add_all(workouts)


    # Add marathon events to marathons tables
    marathons = [
            Marathon(
                name = "Marathon A",
                event_date = date(2026, 12, 12), 
                location = "Gold Coast",
                distance_kms = 10
            ), 
            Marathon(
                name = "Marathon B",
                event_date = date(2025, 10, 8),
                location = "Melbourne",
                distance_kms = 20
            )
        ]
    # Add created marathons to DB and commit changes all changes above to DB
    db.session.add_all(marathons)


    # Add marathon_logs to logs tables
    logs = [
            Log(
                entry_created = date.today(),
                group=groups[0],  
                marathon=marathons[1]
            ), 
            Log(
                entry_created = date.today(),
                group=groups[1],  
                marathon=marathons[0]
            )
        ]
    # Add created logs and commit changes to DB
    db.session.add_all(logs)
    # Commit all changes
    db.session.commit()
    
    print("Tables seeded!")


# Command to drop the tables
@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped!")

