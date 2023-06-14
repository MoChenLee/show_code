def dict_contain(parameter: list, dic: {}):
    for k in parameter:
        if k not in dic:
            return False
    return True
