from fastapi import FastAPI
from .schemas import Blog
from . import models
from .database import engine

app = FastAPI()
models.Base.metadata.create_all(engine)

@app.post('/blog')
def create_blog(request: Blog):
    return request