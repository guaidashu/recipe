"""
author songjie
"""
from tool.db import DBConfig
from tool.function import debug


class DbTest(object):
    def __init__(self):
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()

    def get_columns(self):
        data = {
            "name": "test"
        }
        sql = self.db.getInsertSql(data, "type")
        debug(sql)
