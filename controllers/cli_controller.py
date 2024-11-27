from flask import Blueprint
from init import db
from models.student import Student
from models.teacher import Teacher
from models.course import Course

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

    teachers = [
        Teacher(
            name = "Teacher 1",
            department = "English",
            address = "Brisbane"
        ),
        Teacher(
            name = "Teacher 2",
            department = "Math",
            address = "Gold Coast"
        ),
        Teacher(
            name = "Teacher 3",
            department = "Science",
            address = "Melbourne"
        ),
        Teacher(
            name = "Teacher 4",
            department = "IT",
            address = "Brisbane"
        )
    ]
    
    db.session.add_all(teachers)
    db.session.commit()
    
    courses = [
        Course(
            name = "Course 1",
            duration = 1,
            teacher_id = teachers[0].id
        ),
        Course(
            name = "Course 2",
            duration = 1.5,
            teacher_id = teachers[3].id
        ),
        Course(
            name = "Course 3",
            duration = 2,
            teacher_id = teachers[1].id
        ),
        Course(
            name = "Course 4",
            duration = 4,
            teacher_id = teachers[2].id
        ),
        Course(
            name = "Course 5",
            duration = 1.5,
            teacher_id = teachers[1].id
        )
    ]

    db.session.add_all(courses)
    db.session.commit()

    print("Tables Seeded")