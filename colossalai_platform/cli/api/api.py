import json
import requests
from pydantic import BaseModel

from colossalai_platform.cli.config import Config


class LoginError(Exception):
    pass


class ColossalPlatformApi(BaseModel):
    config: Config
    token: str = ""

    def login(self):
        url = "https://luchentech.com//api/user/login"

        if self.config.username == "" or self.config.password == "":
            raise LoginError("Username or password is empty, please call `cap configure` first")

        payload = json.dumps({
            "username": self.config.username,
            "password": self.config.password,
        })

        headers = {'Content-Type': 'application/json'}

        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=payload,
            verify=False,    # FIXME(ofey404): remove this
        )

        if response.status_code == 200:
            self.token = response.json()['accessToken']
        else:
            raise LoginError(f"Login failed with status code {response.status_code}, body: {response.text}")
