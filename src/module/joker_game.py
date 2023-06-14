import logging
import random


from .item import Item
from .user import User
from src.request.api import api_post
from docs.conf import module_data, play_course

logger = logging.getLogger()


class Joker():
    module_name = "Joker"

    def __init__(self):
        self.joker_data = module_data.get("joker", [])
        self.game_data = {}
        self.special_chapter = {1: 0, 2: 0}  # 怪兽和特殊

    def joker_query(self, name="joker_query"):
        _name = name + "_"
        if not hasattr(self, _name):
            setattr(self, _name, play_course.get(name, {}))
        joker_query = getattr(self, _name)
        data = joker_query.get("data")
        data.update({"instance_id": self.instance_id})
        status, text = api_post(joker_query.get("url"), data)
        if not status:
            if text == 12000:
                self.user_add_system_open("user_add_system_open")
                self.joker_query(name=name)
                return True
            return False
        self.game_data.update(text)
        return True

    # 11002
    def joker_play(self, name="joker_play"):
        _name = name + "_"
        if not hasattr(self, _name):
            setattr(self, _name, play_course.get(name, {}))
        joker_play = getattr(self, _name)
        if self.game_data["state"] == 0:
            data = joker_play.get("data")
            if self.special_chapter[1] and self.special_chapter[2]:
                data.update({"pick_index": random.randint(1, 4), "instance_id": self.instance_id, "type": 1})
                status, text = api_post(joker_play.get("url"), data)
                return True

            else:
                data.update({"pick_index": random.randint(1, 4), "instance_id": self.instance_id, "type": 0})
                status, text = api_post(joker_play.get("url"), data)
                if status:
                    self.game_data.update(text)
                    self.joker_play(name=name)
            return True
        elif self.game_data["state"] == 1:
            data = joker_play.get("data")
            if self.special_chapter[1] and self.special_chapter[2]:
                data.update({"pick_index": random.randint(1, 4), "instance_id": self.instance_id, "type": 3})
                status, text = api_post(joker_play.get("url"), data)
                return True
            else:
                data.update({"pick_index": random.randint(1, 4), "instance_id": self.instance_id, "type": 4})
                status, text = api_post(joker_play.get("url"), data)
                self.special_chapter[1] = 1
                if status:
                    self.game_data.update(text)
                    self.joker_play(name=name)
            return True
        elif self.game_data["state"] == 2:
            data = joker_play.get("data")
            if self.special_chapter[1] and self.special_chapter[2]:
                data.update({"pick_index": random.randint(1, 4), "instance_id": self.instance_id, "type": 2})
                status, text = api_post(joker_play.get("url"), data)
                return True
            else:
                data.update({"pick_index": random.randint(1, 4), "instance_id": self.instance_id, "type": 0})
                status, text = api_post(joker_play.get("url"), data)
                self.special_chapter[2] = 1
                if status:
                    self.game_data.update(text)
                    self.joker_play(name=name)
            return True

    def joker_loop(self, name):
        number = play_course.get(name, {}).get("number", 0)
        if number == 0:
            while True:
                if self.joker_play():
                    return

    def add_item(self, name):
        item_data = play_course.get(name, {})
        data = item_data.get("data")
        data.update({"item_id": 1113005})
        return Item.add_item(item_data.get("url"), data)

    def item_instanceid(self, name):
        instance_data = play_course.get(name, {})
        data = instance_data.get("data")
        data.update({"item_id": 1113005})
        result = User.user_item_instance(instance_data.get("url"), data)
        if result[0]:
            setattr(self, "instance_id", result[1])
            return True
        return False

    def user_add_system_open(self, name):
        data = play_course.get(name, {})
        result = User.user_system_open(data.get("url"), data.get("data"))
        if result:
            return True

    def run(self):
        for func_name in self.joker_data:
            func = getattr(self, func_name)
            if func is not None:
                if not func(func_name):
                    logger.error("{} test error".format(func_name))
                    return
