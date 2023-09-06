import json
import logging
from dataclasses import dataclass

from colossalai_platform.cli.api.types import ApiError, Context

LOGGER = logging.getLogger(__name__)


@dataclass
class User:
    ctx: Context

    def login(self) -> str:
        url = self.ctx.config.api_server + "/api/user/login"

        if self.ctx.config.username == "" or self.ctx.config.password == "":
            raise ApiError("Username or password is empty, please call `cap configure` first")

        response = self.ctx.session.post(
            url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                "username": self.ctx.config.username,
                "password": self.ctx.config.password,
            }),
        )

        if response.status_code == 200:
            self.ctx.token = response.json()['accessToken']
            LOGGER.debug(f"Login success, token: {self.ctx.token}")
        else:
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")
