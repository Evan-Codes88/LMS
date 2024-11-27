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
    
