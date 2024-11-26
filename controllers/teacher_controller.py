from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.teacher import Teacher, teacher_schema, teachers_schema

teachers_bp = Blueprint("teachers", __name__, url_prefix = "/teachers")