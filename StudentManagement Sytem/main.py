from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas

from database import Base, engine, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/students", response_model=schemas.StudentResponse)
def create(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)


@app.get("/students", response_model=list[schemas.StudentResponse])
def get_all(db: Session = Depends(get_db)):
    return crud.get_students(db)


@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def get_one(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update(student_id: int,
           student: schemas.StudentCreate,
           db: Session = Depends(get_db)):

    updated = crud.update_student(db, student_id, student)

    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")

    return updated


@app.delete("/students/{student_id}")
def delete(student_id: int, db: Session = Depends(get_db)):

    student = crud.delete_student(db, student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student deleted successfully"}