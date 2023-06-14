from src.libs.judge_method import dict_contain
from src.request.api import api_post


class Item():

    @staticmethod
    def add_item(url, data):
        if dict_contain(["mid", "item_id", "number"], data):
            status, text = api_post(url, data)
            return status
