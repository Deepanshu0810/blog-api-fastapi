from pydantic import BaseModel
from typing import List

class User(BaseModel):
    username: str
    email: str
    password: str

class Blog(BaseModel):
    title: str
    body: str
    class Config():
        orm_mode = True

class ShowUser(BaseModel):
    username: str
    email: str
    blogs: List[Blog] = []
    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser
    # we created another schema just to make sure that we are not returning the id of the blog to the user
    # orm_mode is used to tell pydantic to read the data even if it is not a dict
    class Config():
        orm_mode = True
