import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path

import click
import yaml
from pydantic import BaseModel

from colossalai_platform.cli.api import ColossalPlatformApi
from colossalai_platform.cli.config import Config

LOGGER = logging.getLogger(__name__)


@dataclass
class BaseCommandContext:
    """This `base` class is the only way to persist
    dataclass-like **kwargs initialization, while we can inject
    code at CommandContext's `__init__` method
    """
    dir: Path = Path.home() / ".colossalai-platform"
    config: Config = Config()
    api: ColossalPlatformApi = None


class CommandContext(BaseCommandContext):

    def __init__(self, **kwargs):
        # set up default value
        super().__init__(**kwargs)

        if self.config_path().is_file():
            self._load_config()
        else:
            click.echo(f"Config doesn't exist on {self.config_path()}, writing default to it")
            self.dump_to_dir()

        LOGGER.debug(f"Config: {self.config}")

        if self.api is None:
            self.api = ColossalPlatformApi(config=self.config)

    def _load_config(self):
        with open(self.config_path(), 'r') as f:
            config_dict = yaml.safe_load(f)
            # update with new data
            self.config = self.config.model_validate(config_dict)

    def dump_to_dir(self):
        self.dir.mkdir(parents=True, exist_ok=True)

        descriptor = self.new_file_700(self.config_path())

        with open(descriptor, 'w') as f:
            config_dict = self.config.model_dump()
            yaml.dump(
                config_dict,
                f,
                sort_keys=False,    # Convert the model to a JSON string using the original field order
            )

    @staticmethod
    def new_file_700(path):
        return os.open(
            path=path,
            flags=(
                os.O_WRONLY    # access mode: write only
                | os.O_CREAT    # create if not exists
                | os.O_TRUNC    # truncate the file to zero
            ),
            mode=0o700)

    def config_path(self) -> Path:
        return self.dir / "config.yaml"
