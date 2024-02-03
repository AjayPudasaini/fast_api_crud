from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type:  str
    