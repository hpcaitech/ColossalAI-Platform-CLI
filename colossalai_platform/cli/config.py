from pydantic import BaseModel, HttpUrl


class Config(BaseModel):
    api_server: str = "https://101.126.46.176"
    username: str = ""
    password: str = ""
    max_upload_chunk_bytes: int = 1024 * 1024 * 1024    # 1 GB
