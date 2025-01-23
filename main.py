from .models import Base

from fastapi import FastAPI
from .database import engine
from fastapi.middleware.cors import CORSMiddleware
from .routers import books

app = FastAPI()
origins = ["*"]    

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


app.include_router(books.router)

