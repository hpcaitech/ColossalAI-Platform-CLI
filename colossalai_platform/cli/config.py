from pydantic import BaseModel


class Config(BaseModel):
    username: str = ""
    password: str = ""
