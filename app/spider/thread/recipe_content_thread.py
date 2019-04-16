"""
author songjie
"""
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from bs4 import BeautifulSoup

from app.spider.common import CommonFunc
from app.spider.recipe_list import RecipeListSpider
from tool.db import DBConfig
from tool.function import debug, curlData

lock = threading.RLock()


class RecipeContentThread(object):
    def __init__(self):
        self.recipe_list = RecipeListSpider()
        self.table_columns = (
            ("id", "int"),
            ("img_url", "varchar"),
            ("video_id", "varchar"),
            ("preparation", "longtext"),
            ("ingredients", "text"),
            ("name", "varchar"),
            ("list_id", "int")
        )
        self.handle_num = 0
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()

    def run(self):
        """
        :return:
        """
        data = self.get_list()
        self.start(data)

    def start(self, data):
        """
        :param data:
        :return:
        """
        thread_pool = ThreadPoolExecutor(max_workers=15)
        task_list = list()
        for item in data:
            task = thread_pool.submit(self.handle_data, item)
            task_list.append(task)
        for i in as_completed(task_list):
            result = i.result()
        debug("本次处理成功 {num} 个线程".format(num=self.handle_num))

    def get_list(self):
        """
        :return:
        """
        data = self.recipe_list.get_list()
        return data

    def handle_data(self, item):
        """
        :param item:
        :return:
        """
        page_resource = self.get_data(item)
        result = self.__handle_data(page_resource, item)
        if result['code'] == 0:
            debug("菜谱存储出错 --> {name}".format(name=item['name']))
        else:
            debug("菜谱存储成功 --> {name}".format(name=item['name']))
            self.__update_status(result['code'])
            lock.acquire()
            self.handle_num = self.handle_num + 1
            lock.release()
        return {"code": 0}

    @classmethod
    def get_data(cls, item):
        """
        :param item:
        :return:
        """
        url = CommonFunc().generate_content_url(item['url'])
        data = curlData(url, open_virtual_ip=True)
        return data

    def __handle_data(self, page_resource, item):
        """
        :param page_resource:
        :param item:
        :return:
        """
        bs = BeautifulSoup(page_resource, "html.parser")
        insert_arr = dict()
        insert_arr['video_id'] = self.__get_video_id(bs)
        insert_arr['img_url'] = self.__get_img_url(page_resource)
        insert_arr['name'] = item['name']
        insert_arr['preparation'] = self.__get_preparation(bs)
        insert_arr['ingredients'] = self.__get_ingredients(bs)
        insert_arr['list_id'] = item['id']
        result = self.__save_data(insert_arr)
        return {'code': result}

    def __save_data(self, insert_arr):
        lock.acquire()
        sql = self.db.getInsertSql(insert_arr, table="content", table_columns=self.table_columns)
        result = self.db.insertLastId(sql, is_close_db=False)
        lock.release()
        return result

    def __update_status(self, recipe_list_id):
        update_arr = {
            "table": "list",
            "set": {"status": "1"},
            "condition": ["id={recipe_list_id}".format(recipe_list_id=recipe_list_id)]
        }
        lock.acquire()
        self.db.update(update_arr, is_close_db=False)
        lock.release()

    @classmethod
    def __get_video_id(cls, bs):
        """
        :param bs:
        :return:
        """
        video_id = bs.find("iframe")
        try:
            video_id = video_id.attrs['src']
            video_id = re.findall('https://www.youtube.com/embed/([\w\W]*?)\?', video_id)[0]
        except Exception as e:
            video_id = ""
            debug("视频播放id获取出错，错误信息：{error}".format(error=e))
        return video_id

    @classmethod
    def __get_img_url(cls, bs):
        # img_url = bs.find("div", attrs={"class": "ytp-cued-thumbnail-overlay-image"})
        try:
            # img_url = img_url.attrs['style']
            img_url = re.findall('"image": "([\w\W]*?)"', str(bs))[0]
        except Exception as e:
            img_url = ""
            debug("菜谱图片链接获取出错，错误信息：{error}".format(error=e))
        return img_url

    @classmethod
    def __get_preparation(cls, bs):
        """
        :param bs:
        :return:
        """
        preparation = bs.find("div", attrs={"class": "cs-recipe-single-preparation"})
        try:
            preparation = preparation.find("ul")
            preparation = str(preparation)
            preparation = re.findall("<ul>([\w\W]*?)<\/ul>", preparation)[0]
        except Exception as e:
            preparation = ""
            debug("菜谱做法获取出错，错误信息：{error}".format(error=e))
        return preparation

    @classmethod
    def __get_ingredients(cls, bs):
        ingredients = bs.find("div", attrs={"class": "cs-ingredients-check-list"})
        ingredients_str = ""
        try:
            ingredients = ingredients.find("ul")
            ingredients = ingredients.find_all("li")
            for k, v in enumerate(ingredients):
                if k == 0:
                    ingredients_str = ingredients_str + v.get_text().strip()
                else:
                    ingredients_str = ingredients_str + "," + v.get_text().strip()
        except Exception as e:
            ingredients_str = ""
            debug("配料获取出错，错误信息：{error}".format(error=e))
        return ingredients_str
