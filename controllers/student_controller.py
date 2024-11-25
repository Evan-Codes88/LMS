from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.student import Student, students_schema, student_schema

students_bp = Blueprint("students", __name__, url_prefix = "/students")

# Read all - /students - GET
@students_bp.route("/")
def get_students():
    stmt = db.select(Student)
    students_list = db.session.scalars(stmt)
    data = students_schema.dump(students_list)
    return data

# Read one - /students/id - GET
@students_bp.route("/<int:student_id>")
def get_student(student_id):
    stmt = db.select(Student).filter_by(id = student_id)
    student = db.session.scalar(stmt)
    if student:
        data = student_schema.dump(student)
        return data
    else:
        return {"message": f"Student with id {student_id} does not exist"}, 404
    

# Create - /students - POST
@students_bp.route("/", methods = ["POST"])
def create_student():
    try:
        # get information from the request body
        body_data = request.get_json()
        # create student instance
        new_student = Student(
            name = body_data.get("name"),
            email = body_data.get("email"),
            address = body_data.get("address")
        )
        # add to the session
        db.session.add(new_student)
        # commit
        db.session.commit()
        # return a response
        return student_schema.dump(new_student), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not null violation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # unique constraint violation
            return {"message": "Email address already in use"}, 409
        
# Delete - /students/id - DELETE
@students_bp.route("/<int:student_id>", methods = ["DELETE"])
def delete_student(student_id):
    # Find the student to be deleted using id
    stmt = db.select(Student).filter_by(id = student_id)
    student = db.session.scalar(stmt)
    # If exists
        # Delete
        # Return Response
    if student:
        db.session.delete(student)
        db.session.commit()
        return {"message": f"Student '{student.name}' was successfully deleted"}
    # Else
        # Return Error Response
    else:
        return {"message": f"Student with id {student_id} does not exist"}, 404
    

# Update - /students/id - PUT, PATCH
@students_bp.route("/<int:student_id>", methods = ["PUT", "PATCH"])
def update_student(student_id):
    try:
        stmt = db.select(Student).filter_by(id = student_id)
        student = db.session.scalar(stmt)
        body_data = request.get_json()

        if student:
            student.name = body_data.get("name") or student.name
            student.email = body_data.get("email") or student.email
            student.address = body_data.get("address") or student.address
            db.session.commit()
            return student_schema.dump(student)
        else:
            return {"message": f"Student with id {student_id} does not exist"}, 404

    except IntegrityError as err:
        return {"message": "Email address already in use"}, 409