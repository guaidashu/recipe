"""
author songjie
"""
import json

from tool.function import debug


class SimpleTest(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    @classmethod
    def test_list_to_str(cls):
        li = {1, 2, 3, 24}
        debug(type(li))

    def test_json(self):
        data = {"ok": "asdada"}
        debug(type(json.dumps(data)))
