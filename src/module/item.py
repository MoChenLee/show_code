from src.libs.judge_method import dict_contain
from src.request.api import api_post


class Item():
    def __init__(self, item_id=0, mid="82466", app_id=703, source="test"):
        self.item_id = item_id
        self.mid = mid
        self.app_id = app_id
        self.source = source

    def add_item(self, data):
        if dict_contain(["number"], data):
            data.update({"mid": self.mid, "item_id": self.item_id, "source": self.source})
            ok, status, text = api_post("/v1/user/item/add", data)
            return ok

    @staticmethod
    def del_item(url, data):
        if dict_contain(["mid", "item_id"], data):
            ok, status, text = api_post(url, data)
            return ok

    def item_instanceid(self):
        ok, status, text = api_post("/v1/user/item_instance_id", {"mid": self.mid, "item_id": self.item_id})
        if ok and status == 200:
            if text.get("instance_id") != "":
                return True, text.get("instance_id")
        return False, ""
