from flask import Blueprint
from init import db
from models.student import Student

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables Created")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables Dropped")

@db_commands.cli.command("seed")
def seed_tables():
    students = [
        Student(
            name = "Student 1",
            email = "student1@email.com",
            address = "Sydney"
        ),
        Student(
            name = "Student 2",
            email = "student2@email.com",
            address = "Melbourne"
        ),
        Student(
            name = "Student 3",
            email = "student3@email.com",
            address = "Gold Coast"
        ),
        Student(
            name = "Student 4",
            email = "student4@email.com",
            address = "Sydney"
        ),
        Student(
            name = "Student 5",
            email = "student5@email.com",
            address = "Gold Coast"
        )
    ]

    db.session.add_all(students)
    db.session.commit()

    print("Tables Seeded")