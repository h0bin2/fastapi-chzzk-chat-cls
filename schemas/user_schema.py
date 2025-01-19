from pydantic import BaseModel
class UserRegister(BaseModel):
    username: str
    password: str
    email: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str