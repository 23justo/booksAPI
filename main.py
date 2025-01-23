import models

from fastapi import FastAPI, Depends, HTTPException, Path
from pydantic import BaseModel, Field, validator
from starlette import status
from typing import Optional
from enum import Enum
from sqlalchemy.orm import Session
from typing import Annotated
from database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://blonde-lissy-justo-1382e3ae.koyeb.app"


]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


class StatusEnum(str, Enum):
    draft = "DRAFT"
    published = "PUBLISHED"


class BookRequest(BaseModel):
    title: str = Field(min_length=3)
    year: int = Field(gt=0)
    author_name: Optional[str] = None
    author_id: Optional[int] = None
    status: StatusEnum


class BookRequestPut(BaseModel):
    title: Optional[str] = None
    year: Optional[int] = None
    author_name: Optional[str] = None
    author_id: Optional[int] = None
    status: Optional[StatusEnum] = None


@app.get("/books")
async def get_books(db: Annotated[Session, Depends(get_db)]):
    return db.query(models.Books).all()


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def post_books(db: db_dependency, book_request: BookRequest):
    if not book_request.author_id and not book_request.author_name:
        raise HTTPException(status_code=422, detail="you need to provide at least author_id or author_name")
    dump_book_request = {
        'title': book_request.title,
        'year': book_request.year,
        'author_id': book_request.author_id,
        'status': book_request.status
    }
    if not db.query(models.Books).get(book_request.author_id) or not dump_book_request['author_id']:            
            authors_model = models.Authors(**{'name': book_request.author_name})
            db.add(authors_model)
            db.flush()
            dump_book_request['author_id'] = authors_model.id
            
    book_model = models.Books(**dump_book_request)
    db.add(book_model)
    db.commit()

@app.put("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, book_request: BookRequestPut, book_id: int = Path(gt=0)):
    
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book_request.title:
        book_model.title = book_request.title
    if book_request.year:
        book_model.year = book_request.year    
    if book_request.author_id:
        book_model.author_id = book_request.author_id
    if book_request.status:
        book_model.status = book_request.status
    db.add(book_model)
    db.commit()
    if book_request.author_name:
        author_model = db.query(models.Authors).filter(models.Authors.id == book_model.author_id).first()
        author_model.name = book_request.author_name
        db.add(author_model)
        db.commit()
    