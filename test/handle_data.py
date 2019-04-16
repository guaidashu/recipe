import re
"""
author songjie
"""
from bs4 import BeautifulSoup

from tool.db import DBConfig
from tool.function import debug


class HandleData(object):
    def __init__(self):
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()

    def handle_category(self):
        category_li = self.__handle_category()
        self.__handle_category_data(category_li)

    @classmethod
    def __handle_category(cls):
        with open("tmp/category_data.txt", "rb") as f:
            page_resource = f.read().decode("utf-8")
            f.close()
        bs_data = BeautifulSoup(page_resource, "html.parser")
        category_ul = bs_data.find_all("ul", attrs={"class": "sub-menu"})
        # only get the next level's li(tag), not include offspring(need to add 'recursive=False')
        return category_ul[0].find_all("li", recursive=False)

    def __handle_category_data(self, category_li, handle_type=1, parent_id=0):
        table_columns = (
            ("id", "int"),
            ("name", "varchar"),
            ("page_num", "longtext"),
            ("nav_type", "int"),
            ("keyword", "varchar"),
            ("parent_id", "int")
        )
        for item in category_li:
            insert_arr = {
                "parent_id": 0,
                "nav_type": 2
            }
            try:
                href = item.find("a").attrs['href']
                try:
                    insert_arr['keyword'] = re.findall('category=([\w\W]*.)', href)[0]
                except Exception as e:
                    debug(e)
                if handle_type == 2:
                    insert_arr['parent_id'] = parent_id
                if href == "#":
                    insert_arr['name'] = item.find("span").getText().strip()
                    insert_arr['nav_type'] = 1
                    sql = self.db.getInsertSql(insert_arr, "type", table_columns=table_columns)
                    lastest_id = self.db.insertLastId(sql, is_close_db=False)
                    if lastest_id == 0:
                        debug("get data error")
                        continue
                    self.__handle_category_data(item.find_all("li"), 2, lastest_id)
                else:
                    insert_arr['name'] = item.getText().strip()
                    sql = self.db.getInsertSql(insert_arr, "type", table_columns=table_columns)
                    self.db.insert(sql, is_close_db=False)
            except Exception as e:
                debug(e)
