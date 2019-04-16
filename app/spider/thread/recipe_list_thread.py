"""
author songjie
"""
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from bs4 import BeautifulSoup

from app.spider.common import CommonFunc
from tool.db import DBConfig
from tool.function import debug, curlData

lock = threading.RLock()


class RecipeListThread(object):
    def __init__(self, page_list, category):
        """
        :param page_list:
        :param category:
        """
        self.page_list = page_list
        self.category = category
        self.handle_num = 0
        # 自己定义字段可以避免重复查询字段的类型自动拼接
        self.table_columns = (
            ("id", "int"),
            ("name", "varchar"),
            ("url", "varchar"),
            ("img_url", "varchar"),
            ("introduce", "text"),
            ("recipe_type_id", "int"),
            ("status", "int"),
            ("page_views", "int")
        )
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()

    def run(self):
        """
        start threading
        :return:
        """
        thread_pool = ThreadPoolExecutor(max_workers=10)
        task_list = list()
        # 添加线程
        for p in self.page_list:
            task = thread_pool.submit(self.get_data, p)
            task_list.append(task)
        debug("本次线程数量：{length}".format(length=len(task_list)))
        # 开始并阻塞线程
        for i in as_completed(task_list):
            result = i.result()
            if result['code'] == 0:
                debug("{category} -- 第{page}页的数据获取完毕".format(category=self.category['keyword'], page=result['page']))
        debug("处理了{length}个线程".format(length=self.handle_num))

    def get_data(self, page):
        """
        :param page:
        :return:
        """
        global lock
        url = CommonFunc().generate_url(page, self.category['keyword'])
        # 获取数据
        page_resource = curlData(url, open_virtual_ip=True)
        # with open("tmp/recipe_list.txt", "rb") as f:
        #     page_resource = f.read().decode("utf-8")
        #     f.close()
        # 处理并存储数据
        self.handle_data(page_resource)
        lock.acquire()
        self.handle_num = self.handle_num + 1
        lock.release()
        return {"code": 0, "page": page}

    def handle_data(self, page_resource):
        """
        :param page_resource:
        :return:
        """
        bs = BeautifulSoup(page_resource, "html.parser")
        li_list = self.__get_li_list(bs)
        lock.acquire()
        for item in li_list:
            insert_arr = dict()
            insert_arr['recipe_type_id'] = self.category['id']
            insert_arr['status'] = 0
            insert_arr['img_url'] = self.__get_img_url(item)
            insert_arr['url'] = self.__get_url(item)
            insert_arr['introduce'] = self.__get_introduce(item)
            insert_arr['page_views'] = self.__get_page_views(item)
            insert_arr['name'] = self.__get_name(item)

            sql = self.db.getInsertSql(insert_arr, table="list", table_columns=self.table_columns)
            result = self.db.insert(sql, is_close_db=False)
            if result == 1:
                debug("插入成功")
            else:
                debug("插入失败")
        lock.release()

    @classmethod
    def __get_li_list(cls, bs):
        container_list = bs.find_all("div", attrs={"class": "cs-recipes-category"})
        li_list = container_list[0].find_all("li", attrs={"class": "cs-recipe"})
        return li_list

    @classmethod
    def __get_img_url(cls, item):
        img_url = item.find("img")
        try:
            img_url = img_url.attrs['src']
        except Exception as e:
            img_url = ""
            debug("图片链接获取出错，错误信息：{error}".format(error=e))
        return img_url

    @classmethod
    def __get_url(cls, item):
        url = item.find("a")
        try:
            url = url.attrs['href']
        except Exception as e:
            url = ""
            debug("详情页链接获取出错，错误信息：{error}".format(error=e))
        return url

    @classmethod
    def __get_introduce(cls, item):
        introduce = item.find_all("span")
        try:
            introduce = introduce[0].get_text().strip()
        except Exception as e:
            introduce = ""
            debug("介绍获取出错，错误信息：{error}".format(error=e))
        return introduce

    @classmethod
    def __get_page_views(cls, item):
        page_views = item.find_all("span")
        try:
            page_views = page_views[1].get_text().strip()
            # 去掉逗号
            page_views = page_views.replace(",", "")
            page_views = page_views.replace(" Plays", "")
        except Exception as e:
            page_views = 0
            debug("浏览量获取出错，错误信息：{error}".format(error=e))
        return page_views

    @classmethod
    def __get_name(cls, item):
        name = item.find("h3")
        try:
            name = name.get_text().strip()
        except Exception as e:
            name = ""
            debug("菜谱名获取出错，错误信息：{error}".format(error=e))
        return name
