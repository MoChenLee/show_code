import json

import requests

local_url = 'http://127.0.0.1:19010'

test_url = 'http://172.16.10.249:19010'

use_url = local_url


def api_post(url, data):
    headers = {'Content-Type': 'application/json'}
    real_url = use_url + url
    response = requests.post(url=real_url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        result = json.loads(response.text)
        if result.get("meta").get('code') == 200:
            return True, result.get("data")
        else:
            return False, result.get("meta").get('code')
    else:
        return False, json.loads(response.text)
