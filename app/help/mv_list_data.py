"""
author songjie
"""
from tool.db import DBConfig
from tool.function import debug


class MvListData(object):
    def __init__(self):
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()

    def run(self):
        self.handle()

    def handle(self):
        data = self.get_data()
        for item in data:
            self.__mv_data(item)

    def __mv_data(self, item):
        select_arr = {
            "table": "list",
            "condition": ["id={id}".format(id=item['list_id'])]
        }
        try:
            data = self.db.select(select_arr, is_close_db=False)[0]
        except Exception as e:
            debug(e)
            return
        sql = self.db.getInsertSql(data, "tmp_list")
        debug(sql)
        result = self.db.insert(sql, is_close_db=False)
        return result

    def get_data(self):
        select_arr = {
            "table": "tmp_content",
        }
        data = self.db.select(select_arr, is_close_db=False)
        return data
