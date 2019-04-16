"""
author songjie
"""
import json

from app.spider.recipe_type import RecipeType
from app.spider.thread.recipe_list_thread import RecipeListThread
from tool.db import DBConfig
from tool.function import debug


class RecipeListSpider(object):
    def __init__(self):
        self.db = DBConfig()
        self.recipe_type = RecipeType()

    def __del__(self):
        self.db.closeDB()

    def run(self):
        """
        start get recipe list
        :return:
        """
        self.get_recipe_list()

    def get_list(self, condition=[], limit=[]):
        """
        :return:
        """
        select_arr = {
            "table": "list",
            "condition": ['status=0']
        }
        data = self.db.select(select_arr, is_close_db=False)
        return data

    def get_category(self):
        """
        get a category's all page num
        :return:
        """
        return self.recipe_type.get_category()

    def get_recipe_list(self):
        """
        :return:
        """
        self.__get_recipe_list()

    def __get_recipe_list(self):
        """
        :return:
        """
        info = self.get_category()
        for item in info:
            self.__get_recipe_list_child(item)

    def __set_status(self, category_id):
        """
        :param category_id:
        :return:
        """
        update_arr = {
            "table": "type",
            "set": {
                "status": 1
            },
            "condition": ['id={category_id}'.format(category_id=category_id)]
        }
        result = self.db.update(update_arr, is_close_db=False)
        if result == 0:
            debug("更新状态出错， 出错原因：unknown")
            return

    def __get_recipe_list_child(self, info):
        """
        :param info:
        :return:
        """
        try:
            page_list = json.loads(info['page_num'])['page_list']
        except Exception as e:
            debug(e)
            self.__set_status(info['id'])
            return
        category = info['keyword']
        if category == "":
            self.__set_status(info['id'])
            return
        page_list = page_list.split(",")
        recipe_list_thread = RecipeListThread(page_list, info)
        recipe_list_thread.run()
        self.__set_status(info['id'])
