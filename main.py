"""
author songjie
"""
from app.help.get_img_url_large import GetImgUrlLarge
from app.help.mv_list_data import MvListData
from app.spider.get_images import GetImages
from app.spider.get_recipe_video import GetRecipeVideo
from app.spider.recipe_content import RecipeContent
from app.spider.recipe_list import RecipeListSpider
from test.db_test import DbTest
from test.handle_data import HandleData
from test.simple_test import SimpleTest
from tool.function import debug

if __name__ == "__main__":
    # get_recipe_video = GetRecipeVideo()
    # get_recipe_video.run()

    # recipe_content = RecipeContent()
    # recipe_content.run()

    # simple_test = SimpleTest()
    # simple_test.test_json()

    # mv_list_data = MvListData()
    # mv_list_data.run()

    # get_img_url_large = GetImgUrlLarge()
    # get_img_url_large.run()
    get_images = GetImages()
    get_images.run()
