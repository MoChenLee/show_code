from docs.conf import Config
from module import *
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(name="main")


class slots_test():
    def __init__(self):
        self.supported_module = self.initialize()

    def initialize(self):
        supported_module = [
            Joker
        ]
        return supported_module

    def run(self):
        for func in self.supported_module:
            logger.info("{} start test".format(func.module_name))
            config = Config.get(func.module_name, None)
            if not config:
                logger.error("{} is no configuration file".format(func.module_name))
                continue
            p = func(**config)
            p.run()
            logger.info("{} test Success".format(func.module_name))
            # print("{} test Success".format(func.module_name))


if __name__ == '__main__':
    project = slots_test()
    project.run()
