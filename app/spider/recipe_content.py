"""
author songjie
"""
from app.spider.thread.recipe_content_thread import RecipeContentThread
from tool.db import DBConfig


class RecipeContent(object):
    def __init__(self):
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()

    @classmethod
    def run(cls):
        recipe_list_thread = RecipeContentThread()
        recipe_list_thread.run()
