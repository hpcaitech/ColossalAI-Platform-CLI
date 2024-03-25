import sys
from typing import Any, Dict, List
from pydantic import BaseModel
import ruamel.yaml
from ruamel.yaml.comments import CommentedMap

class ModelWithYamlComment(BaseModel):
    def dump_str_with_comment(self, f: Any):
        data = self.model_dump()
        yaml = ruamel.yaml.YAML()
        yaml.dump(_parse_comment(data), f)

# All key ended with `{key_name}{postfix}`
# would be treated as comment of {key_name}
COMMENT_POSTFIX_HANDLER = {
    "_comment_before_": lambda commented_map, k, v: commented_map.yaml_set_comment_before_after_key(k, before=v),
    "_comment_after_": lambda commented_map, k, v: commented_map.yaml_set_comment_before_after_key(k, after=v),
    "_comment_eol_": lambda commented_map, k, v: commented_map.yaml_add_eol_comment(v, k)
}

def _parse_comment(data: Dict) -> CommentedMap:
    def _parse(d: Dict | List | Any) -> Any:
        """_parse is a recursive function."""
        if isinstance(d, dict):
            ans = CommentedMap(d)
            comment_keys = []

            for k, v in d.items():
                for postfix, handler in COMMENT_POSTFIX_HANDLER.items():
                    if k.endswith(postfix):
                        key = k[:-len(postfix)]
                        handler(ans, key, v)
                        comment_keys.append(k)
                        break
                ans[k] = _parse(v)

            # remove old comment keys
            for k in comment_keys:
                del ans[k]
            return ans

        elif isinstance(d, list):
            return [_parse(v) for v in d]
        else:
            return d

    return _parse(data)
