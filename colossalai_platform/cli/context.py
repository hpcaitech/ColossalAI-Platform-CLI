import json
from pathlib import Path

import yaml
from pydantic import BaseModel

from colossalai_platform.cli.config import Config


class BaseCommandContext(BaseModel):
    dir: Path = Path.home() / ".cloud-platform"
    config: Config = Config()
    token: str = ""

    def __init__(self, **kwargs):
        # set up default value
        super().__init__(**kwargs)

        if self.config_path().is_file():
            self._load_config()
        else:
            # TODO(ofey404): more formal logging
            print(f"## Config doesn't exist on {self.config_path()}, writing default to it")
            self.dump_to_dir()

        if self._token_path().is_file():
            with open(self._token_path(), 'r') as f:
                self.token = f.read()

    def _load_config(self):
        with open(self.config_path(), 'r') as f:
            config_dict = yaml.safe_load(f)
            # update with new data
            self.config.model_validate(config_dict)

    def dump_to_dir(self):
        self.dir.mkdir(parents=True, exist_ok=True)

        with open(self.config_path(), 'w') as f:
            config_dict = self.config.model_dump()
            yaml.dump(
                config_dict,
                f,
                sort_keys=False,    # Convert the model to a JSON string using the original field order
            )

    def config_path(self) -> Path:
        return self.dir / "config.yaml"

    def _token_path(self) -> Path:
        return self.dir / "token.yaml"
