import logging.config
import random

from .base import BaseService
from src.libs.decorator_result import format_validation
from .user import User

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

    @format_validation
    def request_api(self, *args, **kwargs):
        ok = kwargs.get("processing", False)
        if ok:
            data = kwargs.get("result", {})
            self.game_data.update(data)

    def process(self):
        if self.condition:
            for key, condition in self.condition.items():
                self.user = User()
                if condition:
                    if "user" in condition:
                        self.user.update(condition["user"])
                        self.data = self.user.user_data
                    if "system_open" in condition:
                        self.user.handle_system_open(condition["system_open"])
                    if "add_item" in condition:
                        instance_id = self.user.add_item(condition["add_item"])
                        if instance_id != "":
                            self.data.update({"instance_id": instance_id})
                    # TODO:其它的初始条件
                classification = getattr(self, key, None)
                if not classification:
                    self.logger.error("Config and Premise_config not corresponds")
                    return
                instance_id = self.data["instance_id"]
                self.data["instance_id"] = ""
                if "error" in classification:
                    for k, v in classification["error"]["parameter"].items():
                        if k in classification["error"]["result"]:
                            self.request_api(k, v, classification["error"]["result"][k], processing=False)
                self.data["instance_id"] = instance_id
                if "correct" in classification:
                    setattr(self, "correct", classification["correct"])
                    for k, v in classification["correct"]["parameter"].items():
                        if k in classification["correct"]["result"]:
                            self.request_api(k, v, classification["correct"]["result"][k], processing=True)
        else:
            self.logger.error("Premise_config not module")
            return

        self.joker_loop()
