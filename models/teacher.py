from marshmallow import fields

from init import db, ma


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    department = db.Column(db.String, nullable=False)
    address = db.Column(db.String)

    courses = db.relationship("Course", back_populates="teacher")

class TeacherSchema(ma.Schema):
    courses = fields.List(fields.Nested("CourseSchema", exclude=["teacher"]))
    class Meta:
        fields = ("id", "name", "department", "address", "courses")


teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many=True)