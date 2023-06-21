from docs.conf import Config
from src.libs.decorator_result import format_validation
import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger()


class BaseService():
    def __init__(self):
        self.data = {"mid": "82466", "app_id": 703, "source": "test"}

    def add_item(self, item):
        item_data = Config.get("Item", {}).get("correct", {})
        if not item_data:
            logger.error("add_item is no configuration file")
            return
        data = item_data.get("parameter").get("add_item")
        self.data.update(item)
        self.request_api("add_item", data, item_data.get("result").get("add_item", {}))

    def item_instanceid(self, item):
        instance_data = Config.get("User", {}).get("correct", {})
        if not instance_data:
            logger.error("item_instanceid is no configuration file")
            return
        data = instance_data.get("parameter").get("item_instanceid")
        self.data.update(item)
        self.request_api("item_instanceid", data, instance_data.get("result").get("item_instanceid"), processing=True)
        if getattr(self, "instance_id", None):
            return True
        return False

    @format_validation
    def request_api(self, *args, **kwargs):
        ok = kwargs.get("processing", False)
        if ok:
            pass

    def process(self):
        for k, v in self.error["parameter"].items():
            if k in self.error["result"]:
                self.request_api(k, v, self.error["result"][k], processing=False)
        for k, v in self.correct["parameter"].items():
            if k in self.correct["result"]:
                self.request_api(k, v, self.correct["result"][k], processing=True)

    def run(self):
        self.process()
