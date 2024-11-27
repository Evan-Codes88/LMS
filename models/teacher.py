from marshmallow import fields
from init import db, ma

class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    department = db.Column(db.String(100), nullable = False)
    address = db.Column(db.String(100))

    courses = db.relationship("Course", back_populates = "teacher")

class TeacherSchema(ma.Schema):
    ordered = True
    courses = fields.List(fields.Nested("CourseSchema", exclude = ["teacher", "teacher_id"]))
    class Meta:
        fields = ("id", "name", "department", "address", "courses")

teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many = True)