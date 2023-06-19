from docs.conf import BaseConfig
from src.module.item import Item
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger()


class BaseService():
    def __init__(self):
        self.data = {"mid": "81443", "app_id": 703, "source": "test"}

    def add_item(self, item):
        item_data = BaseConfig.get("add_item", None)
        if not item_data:
            logger.error("add_item is no configuration file")
            return
        data = item_data.get("data")
        data.update(self.data)
        data.update(item)
        return Item.add_item(item_data.get("url"), data)
