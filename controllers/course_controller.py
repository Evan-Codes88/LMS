from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.course import Course, course_schema, courses_schema

courses_bp = Blueprint("courses", __name__, url_prefix = "/courses")

# Read all - /courses - GET
@courses_bp.route("/")
def get_courses():
    stmt = db.select(Course).order_by(Course.id)
    courses_list = db.session.scalars(stmt)
    data = courses_schema.dump(courses_list)
    return data
    

# Read one - /courses/id - GET
@courses_bp.route("/<int:course_id>")
def get_course(course_id):
    stmt = db.select(Course).filter_by(id = course_id).order_by(Course.id)
    course = db.session.scalar(stmt)
    if course:
        data = course_schema.dump(course)
        return data
    else:
        return {"message": f"Course with id {course_id} does not exist"}
    
# Create one - /courses - POST
@courses_bp.route("/", methods = ["POST"])
def create_course():
    try:
        body_data = request.get_json()
        new_course = Course(
            name = body_data.get("name"),
            duration = body_data.get("duration"),
            teacher_id = body_data.get("teacher_id")
        )

        db.session.add(new_course)
        db.session.commit()
        
        return course_schema.dump(new_course), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Course Name already exists"}
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}