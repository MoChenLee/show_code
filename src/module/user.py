from src.libs.judge_method import dict_contain
from src.request.api import api_post


class User():
    @staticmethod
    def user_item_instance(url, data):
        if dict_contain(["mid", "item_id"], data):
            status, text = api_post(url, data)
            return status, text.get("instance_id")

    @staticmethod
    def user_system_open(url, data):
        if dict_contain(["state"], data):
            status, text = api_post(url, data)
            return status
