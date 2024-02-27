from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str

class ShowBlog(BaseModel):
    title: str
    body: str
    # we created another schema just to make sure that we are not returning the id of the blog to the user
    # orm_mode is used to tell pydantic to read the data even if it is not a dict
    class Config():
        orm_mode = True

class User(BaseModel):
    username: str
    email: str
    password: str