from pydantic import BaseModel, HttpUrl


class Config(BaseModel):
    api_server: HttpUrl = "https://luchentech.com"
    username: str = ""
    password: str = ""
    max_upload_chunk_bytes: int = 1024 * 1024 * 1024    # 1 GB
