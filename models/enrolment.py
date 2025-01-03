from datetime import date

from marshmallow import fields, validates
from marshmallow.exceptions import ValidationError

from init import db, ma


class Enrolment(db.Model):
    __tablename__ = "enrolments"
    __table_args__ = (
        db.UniqueConstraint("student_id", "course_id", name="unique_student_course"),
    )

    id = db.Column(db.Integer, primary_key=True)
    enrolment_date = db.Column(db.Date)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)

    student = db.relationship("Student", back_populates="enrolments")
    course = db.relationship("Course", back_populates="enrolments")


class EnrolmentSchema(ma.Schema):

    @validates('enrolment_date')
    def validate_enrolment_date(self, value):
        today = date.today()
        if date.fromisoformat(value) < today:
            raise ValidationError("Enrolment date cannot be in past.")

    student = fields.Nested("StudentSchema", only=["name", "email"])
    course = fields.Nested("CourseSchema", only=["name", "duration"])
    class Meta:
        fields = ("id", "enrolment_date", "student_id", "course_id", "student", "course")


enrolment_schema = EnrolmentSchema()
enrolments_schema = EnrolmentSchema(many=True)