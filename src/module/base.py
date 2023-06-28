from src.libs.decorator_result import format_validation
import logging.config

from src.module.user import User

logging.config.fileConfig('logging.conf')
logger = logging.getLogger()


class BaseService():
    def __init__(self):
        self.data = {"mid": "82466", "app_id": 703, "source": "test"}
        self.condition = None

    @format_validation
    def request_api(self, *args, **kwargs):
        ok = kwargs.get("processing", False)
        if ok:
            pass

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
                if "error" in classification:
                    for k, v in classification["error"]["parameter"].items():
                        if k in classification["error"]["result"]:
                            self.request_api(k, v, classification["error"]["result"][k], processing=False)
                if "correct" in classification:
                    for k, v in classification["correct"]["parameter"].items():
                        if k in classification["correct"]["result"]:
                            self.request_api(k, v, classification["correct"]["result"][k], processing=True)
        else:
            self.logger.error("Premise_config not module")
            return

    def run(self):
        self.process()
