from pathlib import Path
from typing import Generator

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import models
from database import Base, SessionLocal, engine
from schemas import BookCreate, BookOut, BookUpdate

app = FastAPI(title="Book Catalog API")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")


@app.get("/", include_in_schema=False)
def read_index() -> Response:
    return Response(content=(Path(__file__).parent / "static" / "index.html").read_text(encoding="utf-8"), media_type="text/html")


@app.post("/books", response_model=BookOut)
def create_book(payload: BookCreate, db: Session = Depends(get_db)) -> BookOut:
    book = models.Book(
        title=payload.title,
        author=payload.author,
        genre=payload.genre,
        status=payload.status or "available",
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.get("/books", response_model=list[BookOut])
def list_books(db: Session = Depends(get_db)) -> list[BookOut]:
    return db.query(models.Book).order_by(models.Book.id.asc()).all()


@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)) -> BookOut:
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)) -> BookOut:
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}
