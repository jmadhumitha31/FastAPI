from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    age: int
    department: str
    email: str

class StudentResponse(StudentCreate):
    id: int

    class Config:
        from_attributes = True