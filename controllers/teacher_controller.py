from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.teacher import Teacher, teacher_schema, teachers_schema

teachers_bp = Blueprint("teachers", __name__, url_prefix = "/teachers")

# Read all - /teachers - GET
@teachers_bp.route("/")
def get_teachers():
    department = request.args.get("department")
    if department:
        stmt = db.select(Teacher).filter_by(department = department)
    else:
        stmt = db.select(Teacher)
    teachers_list = db.session.scalars(stmt)
    data = teachers_schema.dump(teachers_list)
    return data

# Read one - /teachers - GET
@teachers_bp.route("/<int:teacher_id>")
def get_teacher(teacher_id):
    stmt = db.select(Teacher).filter_by(id = teacher_id)
    teacher = db.session.scalar(stmt)
    if teacher:
        data = teacher_schema.dump(teacher)
        return data
    else:
        return {"message": f"Teacher with id {teacher_id} does not exist"}, 404
    
# Create - /teachers - POST
@teachers_bp.route("/", methods = ["POST"])
def create_teacher():
    try:
        body_data = request.get_json()
        new_teacher = Teacher(
            name = body_data.get("name"),
            department = body_data.get("department"),
            address = body_data.get("address")
        )
        db.session.add(new_teacher)
        db.session.commit()
        return teacher_schema.dump(new_teacher), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "This name Teacher already exists"}

# Delete - /teachers - DELETE
@teachers_bp.route("/<int:teacher_id>", methods = ["DELETE"])
def delete_teacher(teacher_id):
    stmt = db.select(Teacher).filter_by(id = teacher_id)
    teacher = db.session.scalar(stmt)

    if teacher:
        db.session.delete(teacher)
        db.session.commit()
        return {"message": f"Teacher '{teacher.name}' was successfully deleted"}
    else:
        return {"message": f"Teacher with id {teacher_id} does not exist"}, 404
    
# Update - /teachers - PUT, PATCH
@teachers_bp.route("/<int:teacher_id>", methods = ["PATCH", "PUT"])
def update_teacher(teacher_id):
    try:
        stmt = db.select(Teacher).filter_by(id = teacher_id)
        teacher = db.session.scalar(stmt)
        body_data = request.get_json()

        if teacher:
            teacher.name = body_data.get("name") or teacher.name
            teacher.department = body_data.get("department") or teacher.department
            teacher.address = body_data.get("address") or teacher.address
            db.session.commit()
            return teacher_schema.dump(teacher)
        else:
            return {"message": f"Teacher with id {teacher_id} does not exist"}, 404
    except ImportError as err:
        return {"message": "Email address already in use"}, 409
