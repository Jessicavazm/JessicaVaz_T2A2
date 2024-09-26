from datetime import date

from flask import Blueprint

from init import db, bcrypt

from models.user import User
from models.workout import Workout
from models.group import Group
from models.marathon import Marathon
from models.marathon_log import MarathonLog
from models.group_log import GroupLog 


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
            name="User A",
            email="admin_a@email.com",
            password=bcrypt.generate_password_hash("Brazil1.").decode("utf-8"),
            is_admin=True
        ), 
        User(
            name="User C",
            email="user_c@email.com",
            password=bcrypt.generate_password_hash("Brazil2.").decode("utf-8")
        )
    ]
    # Add created users to DB
    db.session.add_all(users)

    # Add workouts to workouts table
    workouts = [
        Workout(
            title="Outside run",
            date=date.today(),
            distance_kms=10,
            calories_burnt=235,
            user=users[0]
        ), 
        Workout(
            title="Outside run",
            date=date.today(),
            distance_kms=10,
            calories_burnt=250,
            user=users[1]
        )
    ]
    # Add created workouts to DB
    db.session.add_all(workouts)

    # Add running groups to groups table
    groups = [
            Group(
                name="Group A",
                date_created=date.today()
            ),
            Group(
                name="Group B",
                date_created=date.today()
            )
        ]
    # Add created groups to DB
    db.session.add_all(groups)
    db.session.commit()

    # Add marathon events to marathons table
    marathons = [
        Marathon(
            name="Marathon A",
            event_date=date(2026, 12, 12),
            location="Gold Coast",
            distance_kms=10
        ),
        Marathon(
            name="Marathon B",
            event_date=date(2025, 10, 8),
            location="Melbourne",
            distance_kms=20
        )
    ]
    # Add created marathons to DB
    db.session.add_all(marathons)

    # Add group_logs to group_logs table 
    group_logs = [
        GroupLog(
            entry_created=date.today(),
            user=users[0],
            group=groups[0]
        ),
        GroupLog(
            entry_created=date.today(),
            user=users[1],
            group=groups[0]
        )
    ]
    # Add created group logs to DB
    db.session.add_all(group_logs)

    # Add marathon_logs to logs table
    marathon_logs = [
        MarathonLog(
            entry_created=date.today(),
            group=groups[0],
            marathon=marathons[1]
        ),
        MarathonLog(
            entry_created=date.today(),
            group=groups[1],
            marathon=marathons[0]
        )
    ]
    # Add created logs to DB
    db.session.add_all(marathon_logs)

    # Commit all changes
    db.session.commit()
    print("Tables seeded!")


# Command to drop the tables
@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped!")
