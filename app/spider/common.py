"""
author songjie
"""
from config.setting import get_config


class CommonFunc(object):
    def __init__(self):
        self.config = get_config()

    def __del__(self):
        pass

    def generate_url(self, page=1, category=""):
        """
        generate a url according to page and category
        :param page:
        :param category:
        :return:
        """
        url = self.config['recipe_list_url']
        suffix = "?screen={page}&category={category}"
        url = url + suffix.format(page=page, category=category)
        return url

    def generate_content_url(self, suffix=""):
        url = self.config['origin_domain']
        return url + "/" + suffix
