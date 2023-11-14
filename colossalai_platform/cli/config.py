from pydantic import BaseModel, HttpUrl


class Config(BaseModel):
    api_server: str = "https://101.126.46.176"
    username: str = ""
    password: str = ""
    max_upload_chunk_bytes: int = 100 * 1024 * 1024    # 100MB

    def check_format(self) -> "Config":
        if not self.api_server.startswith("http"):
            self.api_server = "https://" + self.api_server
        if self.api_server.endswith("/"):
            self.api_server = self.api_server[:-1]

        return self
