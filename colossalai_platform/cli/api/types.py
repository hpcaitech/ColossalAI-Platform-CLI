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
            if self.token == "":
                raise LoginRequiredError()
            headers["Authorization"] = "Bearer " + self.token
        return headers
