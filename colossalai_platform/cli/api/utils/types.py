from dataclasses import dataclass

import requests

from colossalai_platform.cli.config import Config


class ApiError(Exception):
    pass


class LoginRequiredError(Exception):

    def __init__(self, message="Login required"):
        super().__init__(message)


@dataclass
class Context:
    config: Config
    token: str = ""
    session: requests.Session = requests.Session()

    def headers(
            self,
            login=False,
    ):
        headers = {
            'Content-Type': 'application/json',
        }
        if login:
            headers = {
                **headers,
                **self.bearer_token_header(),
            }
        return headers

    def bearer_token_header(self) -> dict:
        if self.token == "":
            raise LoginRequiredError()
        return {
            "Authorization": "Bearer " + self.token,
        }
