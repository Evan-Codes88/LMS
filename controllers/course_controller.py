from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.course import Course, course_schema, courses_schema

course_bp = Blueprint("courses", __name__, url_prefix = "/courses")

