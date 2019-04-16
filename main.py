"""
author songjie
"""
from app.spider.recipe_content import RecipeContent
from app.spider.recipe_list import RecipeListSpider
from test.db_test import DbTest
from test.handle_data import HandleData
from test.simple_test import SimpleTest
from tool.function import debug


if __name__ == "__main__":
    recipe_content = RecipeContent()
    recipe_content.run()
    # simple_test = SimpleTest()
    # simple_test.test_json()
