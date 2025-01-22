from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


app = FastAPI()


class Book:
    id: int
    title: str
    year: int
    author_id: int
    status: str

    def __init__(self, id, title, year, author_id, status):
        self.id = id
        self.title = title
        self.year = year
        self.author_id = author_id
        self.status = status


class StatusEnum(str, Enum):
    draft = "DRAFT"
    published = "PUBLISHED"


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    year: int = Field(gt=0)
    author_id: int
    status: StatusEnum



books = [
    Book(1, 'test', 1111, 1, 'draft'),
    Book(2, 'test2', 2222, 2, 'published'),
    Book(3, 'test3', 3333, 3, 'draft')

]

@app.get("/books")
async def get_books():
    return books

@app.post("/books")
async def post_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())    
    books.append(new_book)

