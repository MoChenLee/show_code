Config = {
    "Joker": {
        "error": {
            "parameter": {
                "joker_query": {"url": "/v1/joker_game/query", "data": {"instance_id": "1"}},
                "joker_play_1": {"url": "/v1/joker_game/play",
                                 "data": {"pick_index": 0, "type": 0, "instance_id": "1"}},
                "joker_play_2": {"url": "/v1/joker_game/play", "data": {"pick_index": 1, "type": 0, "instance_id": "1"}}
            },
            "result": {
                "joker_query": {"code": 13000},
                "joker_play_1": {"code": 11055},
                "joker_play_2": {"code": 13000}
            },
        },
        "correct": {
            "parameter": {
                "joker_query": {"url": "/v1/joker_game/query", "data": {"instance_id": "1"}},
                "joker_play": {"url": "/v1/joker_game/play", "data": {"pick_index": 1, "type": 0, "instance_id": "1"}}
            },
            "result": {
                "joker_query": {"key_list": ["cur_chapter", "total_chapter", "special_chapter", "state"],
                                "key_dict": {"cur_chapter": (1, 30), "total_chapter": (1, 30), "state": [0, 1, 2]},
                                "type_dict": {"cur_chapter": "int", "total_chapter": "int", "special_chapter": "list",
                                              "state": "int"}},
                "joker_play": {"key_list": ["cur_chapter", "state", "mail_instance_id"],
                               "key_dict": {"cur_chapter": (1, 30), "state": [0, 1, 2]},
                               "type_dict": {"cur_chapter": "int", "state": "int", "mail_instance_id": "str"}}
            }}
    },
    "Item": {
        "correct": {
            "parameter": {
                "add_item": {"url": "/v1/user/item/add", "data": {"item_id": 1, "number": 1}},
            },
            "result": {
            }}
    },
    "User": {
        "correct": {
            "parameter": {
                "item_instanceid": {"url": "/v1/user/item_instance_id", "data": {"item_id": 1}},
            },
            "result": {
                "item_instanceid": {"key_list": ["instance_id"], "key_dict": {}, "type_dict": {"instance_id": "str"}}}
        }
    }
}
