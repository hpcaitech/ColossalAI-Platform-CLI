import yaml
from pydantic import BaseModel
from pathlib import Path

# The directory and the config file
CONFIG_DIR = Path.home() / ".cloud-platform"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
TOKEN_FILE = CONFIG_DIR / "config.yaml"


# Your config class
class Config(BaseModel):
    field1: str
    field2: int
    # Define your fields here


def load_or_create_config() -> Config:
    """Load the config if it exists at the default place,
    otherwise create it.
    """
    try:
        return _load_config()
    except FileNotFoundError:
        _init_config()
        return _load_config()


def _load_config() -> Config:
    with open(CONFIG_FILE, 'r') as f:
        config_data = yaml.safe_load(f)
        config = Config(**config_data)
        return config


def _init_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(Config().dict(), f)
