import io
import unittest
from typing import Dict, List

from colossalai_platform.cli.utils.pydantic_model_with_yaml_comment import ModelWithYamlComment

class TestModelWithYamlComment(unittest.TestCase):
    def test_dump(self):
        """This is the example usage of ModelWithYamlComment."""
        output = io.StringIO()
        Config().dump_str_with_comment(output)
        print()
        self.assertEqual(
            output.getvalue(),
"""entry: foo
dict_entry:
  foo: bar
  bar: baz
# comment before list
list_entry:
- 1
- 2
- 3
nested_entry:
  entry: foo  # nested EOL comment
  dict_entry:
  # nested comment after dict
    foo: bar
""")

# Helpers
class NestedConfig(ModelWithYamlComment):
    entry: str = "foo"
    entry_comment_eol_: str = "nested EOL comment"

    dict_entry: Dict[str, str] = {
        "foo": "bar",
    }
    dict_entry_comment_after_: str = "nested comment after dict"

class Config(ModelWithYamlComment):
    entry: str = "foo"
    dict_entry: Dict[str, str] = {
        "foo": "bar",
        "bar": "baz"
    }

    list_entry_comment_before_: str = "comment before list"
    list_entry: List[int] = [1, 2, 3]

    nested_entry: NestedConfig = NestedConfig()
