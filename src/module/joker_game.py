import logging.config
import random

from .base import BaseService
from src.libs.decorator_result import format_validation

logging.config.fileConfig('logging.conf')


class Joker(BaseService):
    module_name = "Joker"

    def __init__(self, **kwargs):
        super().__init__()
        self.logger = logging.getLogger(name=self.module_name)
        self.__dict__.update(**kwargs)
        self.game_data = {}
        self.special_chapter = {1: 0, 2: 0}  # 怪兽和特殊
        self.over = False

    def joker_play(self):
        joker_play = self.correct["parameter"]["joker_play"]
        joker_play_result = self.correct["result"]["joker_play"]
        if self.game_data["state"] == 0:
            if (self.special_chapter[1] and self.special_chapter[2]) or self.game_data["cur_chapter"] == self.game_data[
                "total_chapter"] or self.over:
                joker_play["data"].update({"pick_index": random.randint(1, 4), "type": 1})
                self.request_api("joker_play", joker_play, joker_play_result, processing=True)
                self.over = True
                return False
            else:
                joker_play["data"].update({"pick_index": random.randint(1, 4), "type": 0})
                self.request_api("joker_play", joker_play, joker_play_result, processing=True)
            return True
        elif self.game_data["state"] == 1:
            if self.special_chapter[1] and self.special_chapter[2] or self.game_data["cur_chapter"] == self.game_data[
                "total_chapter"] or self.over:
                joker_play["data"].update({"pick_index": random.randint(1, 4), "type": 3})
                self.request_api("joker_play", joker_play, joker_play_result, processing=True)
                self.over = True
                return False
            else:
                joker_play["data"].update({"pick_index": random.randint(1, 4), "type": 5})
                self.request_api("joker_play", joker_play, joker_play_result, processing=True)
                self.special_chapter[1] = 1
            return True
        elif self.game_data["state"] == 2:
            if self.special_chapter[1] and self.special_chapter[2] or self.game_data["cur_chapter"] == self.game_data[
                "total_chapter"] or self.over:
                joker_play["data"].update({"pick_index": random.randint(1, 4), "type": 2})
                self.request_api("joker_play", joker_play, joker_play_result, processing=True)
                self.over = True
                return False
            else:
                joker_play["data"].update({"pick_index": random.randint(1, 4), "type": 4})
                self.request_api("joker_play", joker_play, joker_play_result, processing=True)
                self.special_chapter[2] = 1
            return True

    def joker_loop(self):
        number = 10
        while number > 0:
            if not self.joker_play():
                return
            number -= 1
        if not self.over:
            self.over = True
            self.joker_play()

    def handle_item(self):
        if not self.item_instanceid({"item_id": 1113005}):
            self.add_item({"item_id": 1113005, "number": 1})
            self.item_instanceid({"item_id": 1113005})
            if not getattr(self, "instance_id"):
                self.logger.error("add_item and item_instanceid error!")
                return False
        self.data.update({"instance_id": self.instance_id})
        return True

    @format_validation
    def request_api(self, *args, **kwargs):
        ok = kwargs.get("processing", False)
        if ok:
            data = kwargs.get("result", {})
            if "instance_id" in data and data["instance_id"] != "":
                setattr(self, "instance_id", data["instance_id"])
                return
            self.game_data.update(data)

    def process(self):
        for k, v in self.error["parameter"].items():
            if k in self.error["result"]:
                self.request_api(k, v, self.error["result"][k], processing=False)
        if not self.handle_item():
            return
        for k, v in self.correct["parameter"].items():
            if k in self.correct["result"]:
                self.request_api(k, v, self.correct["result"][k], processing=True)
        self.joker_loop()
