from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
from ..models import Books, Authors
import pytest
from ..routers.books import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass = StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture
def test_books():
    book = Books(
        title="testing 101",
        year="2025",
        author_id="1",
        status="Published"
    )

    db = TestingSessionLocal()
    db.add(book)
    db.commit()
    yield book
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM books;"))
        connection.commit()

@pytest.fixture
def test_authors():
    author = Authors(
        id=1,
        name="Justo"
    )

    db = TestingSessionLocal()
    db.add(author)
    db.commit()
    yield author
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM authors;"))
        connection.commit()

def test_read_all_books(test_books):
    response = client.get("/books")    
    assert response.status_code == 200
    clean_response = response.json()
    assert clean_response[0]['title'] == "testing 101"

def test_read_all_authors(test_authors):
    response = client.get("/authors")    
    assert response.status_code == 200
    clean_response = response.json()
    assert clean_response[0]['name'] == "Justo"

def test_create_book(test_authors):
    request_data={
        "title":"testing 101",
        "year":2025,
        "author_id":1,
        "status":"PUBLISHED"
    }

    response = client.post('/books', json=request_data)
    assert response.status_code == 201
    db = TestingSessionLocal()
    model = db.query(Books).filter(Books.id == 1).first()
    assert model.title == request_data.get('title')
    assert model.year == request_data.get('year')
    assert model.status == request_data.get('status')

def test_update_book(test_authors):
    request_data={
        "title":"testing 202",
        "year":2025,
        "author_id":1,
        "status":"PUBLISHED"
    }
    response = client.put('/books/1', json=request_data)
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Books).filter(Books.id == 1).first()
    assert model.title == 'testing 202'




