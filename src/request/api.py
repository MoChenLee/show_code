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
        return True, result.get("meta").get('code'), result.get("data")
    else:
        return False, response.status_code, json.loads(response.text)
