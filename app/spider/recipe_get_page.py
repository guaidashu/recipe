"""
author songjie
"""
import json

from bs4 import BeautifulSoup

from app.spider.common import CommonFunc
from app.spider.recipe_type import RecipeType
from tool.db import DBConfig
from tool.function import debug, curlData


class RecipeGetPage(object):
    def __init__(self):
        self.db = DBConfig()
        recipe_type = RecipeType()
        self.category = recipe_type.get()

    def __del__(self):
        self.db.closeDB()

    def get(self):
        """
        :return:
        """
        self.__get_recipe_page()

    def __get_recipe_page(self):
        """
        :return:
        """
        for item in self.category:
            url = CommonFunc().generate_url(category=item['keyword'])
            try:
                self.__get_recipe_page_data(url, item['id'])
            except Exception as e:
                debug("页面数量抓取出错，出错信息：{error}".format(error=e))

    def __get_recipe_page_data(self, url, recipe_category_id):
        """
        :param url:
        :param recipe_category_id:
        :return:
        """
        page_resource = curlData(url, open_virtual_ip=True)
        # with open("tmp/category_page_data.txt", "rb") as f:
        #     page_resource = f.read().decode("utf-8")
        #     f.close()
        bs = BeautifulSoup(page_resource, "html.parser")
        page_ul = bs.find_all("ul", attrs={"class": "page-numbers"})
        # remove prev page and next page
        for k, v in enumerate(page_ul[0]('a', attrs={"class": "next"})):
            v.extract()
        page_a = page_ul[0].find_all("a")
        page_span = page_ul[0].find("span")
        page_list = ""
        for k, v in enumerate(page_a):
            if k == 0:
                page_list = page_list + str(v.get_text()).strip()
            else:
                page_list = page_list + "," + str(v.get_text()).strip()
        page_list = page_list + "," + page_span.get_text().strip()
        page_list = {
            "page_list": page_list
        }
        # update to mysql
        update_arr = {
            "table": "type",
            "set": {
                "page_num": json.dumps(page_list)
            },
            "condition": ['id={id}'.format(id=recipe_category_id)]
        }
        result = self.db.update(update_arr, is_close_db=False)
        if result == 1:
            debug("id为{id}的菜谱类型页面数据抓取成功".format(id=recipe_category_id))
        else:
            debug("id为{id}的菜谱类型页面数据抓取失败".format(id=recipe_category_id))
        # debug(page_list)
