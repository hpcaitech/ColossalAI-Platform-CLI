from colossalai_platform.cli.api.dataset import Dataset
from colossalai_platform.cli.api.types import Context
from colossalai_platform.cli.api.user import User
from colossalai_platform.cli.config import Config


class ColossalPlatformApi:

    def __init__(self, config: Config):
        self.ctx = Context(config)
        self._user = User(self.ctx)
        self._dataset = Dataset(self.ctx)

    def user(self) -> User:
        return self._user

    def dataset(self) -> Dataset:
        return self._dataset
