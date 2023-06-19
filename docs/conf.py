test_module = ["joker"]
module_data = {
    "joker": ["add_item", "item_instanceid", "joker_query", "joker_play"],

}

play_course = {
    "add_item": {"url": "/v1/user/item/add", "data": {"mid": "81443", "item_id": 1, "number": 1, "source": "测试"}},
    "joker_query": {"url": "/v1/joker_game/query", "data": {"mid": "81443", "instance_id": "1"}},
    "joker_play": {"url": "/v1/joker_game/play",
                   "data": {"mid": "81443", "pick_index": 0, "type": 0, "instance_id": "1"}},
    "item_instanceid": {"url": "/v1/user/item_instance_id", "data": {"mid": "81443", "item_id": 1}},
    "user_add_system_open": {"url": "/v1/joker_game/system", "data": {"mid": "81443", "state": 1}},
    "del_item": {"url": "/v1/user/item/del", "data": {"mid": "81443", "item_id": 1, "source": "测试"}}
}
BaseConfig = {
    "add_item": {"url": "/v1/user/item/add", "data": {"item_id": 1, "number": 1, }},
}

Config = {
    "Joker": {
        "parameter": {
            "joker_query": {"url": "/v1/joker_game/query", "data": {"instance_id": "1"}},
            "joker_play": {"url": "/v1/joker_game/play", "data": {"pick_index": 0, "type": 0, "instance_id": "1"}}
        },
        "result": {
            "joker_query": {"url": "/v1/joker_game/query", "data": {"instance_id": "1"}},
            "joker_play": {"url": "/v1/joker_game/play", "data": {"pick_index": 0, "type": 0, "instance_id": "1"}}
        }
    }
}
