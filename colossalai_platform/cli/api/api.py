from colossalai_platform.cli.api.dataset import Dataset
from colossalai_platform.cli.api.model import Model
from colossalai_platform.cli.api.types import Context
from colossalai_platform.cli.api.user import User
from colossalai_platform.cli.api.project import Project
from colossalai_platform.cli.config import Config


class ColossalPlatformApi:

    def __init__(self, config: Config):
        self.ctx = Context(config)
        self._user = User(self.ctx)
        self._dataset = Dataset(self.ctx)
        self._project = Project(self.ctx)
        self._model = Model(self.ctx)

    def user(self) -> User:
        return self._user

    def dataset(self) -> Dataset:
        return self._dataset

    def project(self) -> Project:
        return self._project

    def model(self) -> Model:
        return self._model
