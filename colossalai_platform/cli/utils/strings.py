import string
import random
from dataclasses import asdict

import yaml


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def yaml_dump_dataclass(dataclass):
    if isinstance(dataclass, list):
        ans = yaml.dump([asdict(item) for item in dataclass], default_flow_style=False, sort_keys=False)
    else:
        ans = yaml.dump(asdict(dataclass), default_flow_style=False, sort_keys=False)

    # remove the trailing newline,
    # As the output is often used to format a multiline string:
    #
    # f"""Available images:
    # {yaml_dump_dataclass(images)}
    # ... Other content ...
    # """
    return ans.strip()
