from datetime import date

from flask import Blueprint
from init import db, bcrypt

from models.user import User
from models.workout import Workout
from models.group import Group
from models.marathon import Marathon
from models.marathon_log import Log


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
    db.session.add_all(users)
    

    workouts = [
        Workout(
        date = date.today(),
        distance_kms = 10,
        duration_minutes = 60,
        calories_burnt = 235,
        user = users[0]
    ), Workout(
        date = date.today(),
        distance_kms = 10,
        duration_minutes = 30,
        calories_burnt = 250,
        user = users[1]
    )]
    db.session.add_all(workouts)


    groups = [
            Group(
                name = "Group A",
                date_created = date.today(),
                experience_level = "Intermediate",
                members_capacity = 5,
                created_by = "Jess",
                user = users[1]
            ), 
            Group(
                name = "Group B",
                date_created = date.today(),
                experience_level = "Advanced",
                members_capacity = 3,
                created_by = "Iryna",
                user = users[0]
            )
        ]
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
    db.session.add_all(logs)


    db.session.commit()
    print("Tables seeded!")


# Command to drop the tables
@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped!")

