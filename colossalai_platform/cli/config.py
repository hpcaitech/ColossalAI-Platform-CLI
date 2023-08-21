from pydantic import BaseModel, HttpUrl


class Config(BaseModel):
    api_server: HttpUrl = "https://luchentech.com"
    username: str = ""
    password: str = ""
