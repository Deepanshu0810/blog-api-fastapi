from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn

app = FastAPI()

@app.get("/blog")   #path operation decorator; operation; path
# path operation function
def index(limit:int = 10, published:bool = True, sort: Optional[str] = None): #query parameter
    if published:
        return {"data": f"blog list {limit} published blogs"}
    else:
        return {"data": f"blog list {limit}"}


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "all unpublished blogs"}

# dynamic paths come after static paths
@app.get("/blog/{id}")
def show(id: int): #pydantic model
    return {"data":id}


@app.get("/blog/{id}/comments")
def comments(id:int, limit:int = 10): #query parameter to get 10 comments
    return {"data": {"1", "2"}}

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post("/blog")
def create_blog(request: Blog): #request body
    return {"data": f"Blog is created with title as {request.title}"} 