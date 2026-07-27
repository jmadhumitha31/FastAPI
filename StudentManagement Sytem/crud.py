from sqlalchemy.orm import Session
from models import Student

def create_student(db: Session, student):
    new_student = Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


def get_students(db: Session):
    return db.query(Student).all()


def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


def update_student(db: Session, student_id: int, student):
    db_student = db.query(Student).filter(Student.id == student_id).first()

    if db_student:
        db_student.name = student.name
        db_student.age = student.age
        db_student.department = student.department
        db_student.email = student.email

        db.commit()
        db.refresh(db_student)

    return db_student


def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student:
        db.delete(student)
        db.commit()

    return student