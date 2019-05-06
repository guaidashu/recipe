"""
author songjie
"""
import re

from tool.db import DBConfig
from tool.function import debug


class GetImgUrlLarge(object):
    def __init__(self):
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()

    def run(self):
        self.handle()

    def handle(self):
        data = self.get_data()
        for item in data:
            result = self.__handle(item)
            if result['result_1'] == 1 and result['result_2'] == 1 and result['result_3'] == 1:
                debug(item['img_url'])
            else:
                break

    def __handle(self, item):
        img_url = item['img_url']
        try:
            s = re.findall('squarethumbnails\/([\w\W]*.)', img_url)[0]
        except Exception as e:
            s = ''
            debug(e)
        if s == '':
            return
        s = 'http://www.laurainthekitchen.com/largethumbnails/' + s
        result = self.__update_data(s, item)
        return result

    def __update_data(self, s, item):
        update_arr_list = {
            "table": "list",
            "set": {
                "img_url_large": s,
                "status": 1
            },
            "condition": ["id={id}".format(id=item['id'])]
        }
        result_1 = self.db.update(update_arr_list, is_close_db=False)
        del update_arr_list['set']['status']
        update_arr_list['table'] = "tmp_list"
        result_2 = self.db.update(update_arr_list, is_close_db=False)
        update_arr_list['table'] = "content"
        update_arr_list['condition'] = ["list_id={id}".format(id=item['id'])]
        result_3 = self.db.update(update_arr_list, is_close_db=False)
        return {"result_1": result_1, "result_2": result_2, "result_3": result_3}

    def get_data(self):
        select_arr = {
            "table": "list",
            "columns": ["img_url", "id"],
            "condition": ["status=0"]
        }
        data = self.db.select(select_arr, is_close_db=False)
        return data
