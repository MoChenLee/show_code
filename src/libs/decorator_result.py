import functools

from src.request.api import api_post


def format_validation(func):
    """
    预期结果对比
    """

    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        data = args[1].get("data")
        data.update(self.data)
        ok, status, result = api_post(args[1].get('url'), data)
        if not ok:
            self.logger.error("{} request api error!".format(args[0]))
            return
        for k, v in args[2].items():
            if k == "code":
                if status != v:
                    self.logger.error("{} {}_{} not as expected {}".format(args[0], k, status, v))
                    return
            elif k == "key_list":
                for key in v:
                    if key not in result:
                        self.logger.error("{} {}_{} not as expected".format(args[0], k, key))
                        return
            elif k == "key_dict":
                for key, value in v.items():
                    if type(value) is tuple:
                        if result[key] < value[0] or result[key] > value[1]:
                            self.logger.error(
                                "{} {}_{}_{} not as expected {}".format(args[0], k, key, result[key], value))
                            return
                    elif type(value) is list:
                        if result[key] not in value:
                            self.logger.error(
                                "{} {}_{}_{} not as expected {}".format(args[0], k, key, result[key], value))
                            return
                    elif type(value) is str or type(value) is int:
                        if result[key] != value:
                            self.logger.error(
                                "{} {}_{}_{} not as expected {}".format(args[0], k, key, result[key], value))
                            return
            elif k == "type_dict":
                for key, value in v.items():
                    if type(result[key]).__name__ != value:
                        self.logger.error("{} {}_{}_{} not as expected {}".format(args[0], k, key, result[key], value))
                        return
        return func(self, *args, **kwargs, result=result)

    return wrap
