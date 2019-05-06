"""
author songjie
"""
from pytube import YouTube

from tool.db import DBConfig
from tool.function import debug


class GetRecipeVideo(object):
    def __init__(self):
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()

    def run(self):
        self.download()

    def download(self):
        data = self.get_tmp_content()
        self.__download(data)

    def __download(self, data):
        for item in data:
            url = "https://www.youtube.com/watch?v=%s" % item['video_id']
            debug("开始抓取：--> {video_id}".format(video_id=item['video_id']))
            try:
                youtube = YouTube(url)
                youtube.streams.filter(subtype="mp4").first().download("/Users/cpx/code/py/recipe/data/recipe/",
                                                                       filename=item['video_id'])
                self.__update_data(item['id'])
            except Exception as e:
                debug(e)

    def __update_data(self, list_id):
        """
        :param list_id:
        :return:
        """
        update_arr = {
            "table": "tmp_content",
            "set": {
                "status": 1
            },
            "condition": ['id={list_id}'.format(list_id=str(list_id))]
        }
        result = self.db.update(update_arr, is_close_db=False)
        return result

    def get_tmp_content(self):
        data = self.db.select({"table": "tmp_content", "columns": ['id', 'video_id'], "condition": ['status=0']},
                              is_close_db=False)
        return data

    def handle_data(self):
        self.move_data()
        # data = self.get_data()

    def get_data(self):
        select_arr = {
            "table": "recipe_content"
        }
        data = self.db.select(select_arr, is_close_db=False)
        return data

    def move_data(self):
        category = self.get_category()
        for item in category:
            data = self.get_list_by_type_id(item['id'])
            self.__move_data(data)

    def __move_data(self, data):
        for item in data:
            content = self.get_content_by_list_id(item['id'])
            try:
                content = content[0]
                content['status'] = 0
                self.__insert_data(content)
            except Exception as e:
                debug(e)

    def __insert_data(self, insert_arr):
        sql = self.db.getInsertSql(insert_arr, "tmp_content")
        result = self.db.insert(sql, is_close_db=False)
        return result

    def get_list_by_type_id(self, type_id):
        data = self.db.select({
            "table": "list",
            "condition": ['recipe_type_id={type_id}'.format(type_id=type_id)],
            "limit": [0, 20]
        }, is_close_db=False)
        return data

    def get_content_by_list_id(self, list_id):
        data = self.db.select({
            "table": "content",
            "columns": ['video_id', 'list_id'],
            "condition": ["list_id={list_id}".format(list_id=str(list_id))]
        }, is_close_db=False)
        return data

    def get_category(self):
        data = self.db.select({"table": "type", "condition": ['keyword<>""']}, is_close_db=False)
        return data
