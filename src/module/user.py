import json
import time

from src.libs.judge_method import dict_contain
from src.libs.mysql import mysql
from src.libs.reids import m_redis
from src.libs.time import today_time, time_difference
from src.module.item import Item
from src.request.api import api_post


class User():
    def __init__(self, mid="82466", app_id=703, source="test"):
        self.mid = mid
        self.app_id = app_id
        self.source = source

    @property
    def user_data(self):
        return {"mid": self.mid, "app_id": self.app_id, "source": self.source}

    @staticmethod
    def user_item_instance(url, data):
        if dict_contain(["mid", "item_id"], data):
            ok, status, text = api_post(url, data)
            if status == 200:
                return ok, text.get("instance_id")
            return False, ""

    @staticmethod
    def user_system_open(url, data):
        if dict_contain(["state"], data):
            ok, status, text = api_post(url, data)
            return ok

    def update(self, user):
        self.__dict__.update(user)

    def handle_system_open(self, param):
        for k, v in param.items():
            if "system_name" == k:
                s_break = False
                sql = "select `id`,`system_open_plan`,`mids` from `system_open_configs` where `name` = %s"
                results = mysql.execute(sql, (v,), True)
                for row in results:
                    if row[1] == "test":
                        if row[2]:
                            mids = row[2].split(",")
                            if self.mid not in mids:
                                mids.append(self.mid)
                                sql = "update `system_open_configs` set `mids`=%s where `id` = %s"
                                result = mysql.execute(sql, (mids, row[0]))
                                time.sleep(60)
                        else:
                            sql = "update `system_open_configs` set `mids`=%s where `id` = %s"
                            result = mysql.execute(sql, (self.mid, row[0]))
                            time.sleep(60)
                        s_break = True
                        break
                if not s_break:
                    sql = "insert into `system_open_configs` (`system_open_plan`,`name`,`mids`,`start_time`,`end_time`) values(%s, %s, %s, %s, %s)"
                    result = mysql.execute(sql, (
                        "test", v, self.mid, today_time(), time_difference(year=1)))
                    time.sleep(60)

    def add_item(self, param):
        item = Item(item_id=param["item_id"], mid=self.mid, source=param.get("source", "test"))
        ok, instance_id = item.item_instanceid()
        if not ok:
            item.add_item({"number": param.get("number", 1)})
            ok, instance_id = item.item_instanceid()
            if ok:
                return instance_id
            return ""
        return instance_id

    def machine_spin(self):
        stream_name = 'slots:server_event'
        data = {"collection_ids": [4], "SDKVersion": None, "app_id": self.app_id, "is_power_machine": 0,
                "bet_plan": "default",
                "appsflyerData": {"af_status": "Organic"},
                "device": {"locale": "US", "device_type": "ios", "timezone": 28800, "app_version": "6.6.0"},
                "log_time": "2021-11-16T07:14:29.817Z",
                "data": {"last_pay_time": 0, "name": "SpinClicked",
                         "extra": {"id": 1865,
                                   "event": {"code": None, "uid": "625581637046869.1340735", "BetListTotalCount": 11,
                                             "UserID": "4AE0B1EE-32CF-4BD3-8B08-5FE108A2C1F2",
                                             "topic": "Message",
                                             "VIPTotalPoint": 480,
                                             "CurrentBalance": 1886674,
                                             "CurrentBetNum": 1000000,
                                             "WinCoins": 0.0,
                                             "CurrentMachine": "HoneyLuck",
                                             "TotalLoginDays": 1,
                                             "CurrentBetIndex": 3,
                                             "score": 41,
                                             "outComeData": [{"subId": "",
                                                              "SRs": [
                                                                  ["L01", "L01",
                                                                   "L01", "H02"],
                                                                  ["H02", "H02",
                                                                   "H02", "H02"],
                                                                  ["L02", "L02",
                                                                   "L02", "L02"],
                                                                  ["H02", "H02",
                                                                   "L01", "L01"],
                                                                  ["L03", "L03",
                                                                   "L03", "L01"]],
                                                              "score": 41,
                                                              "winD": {}, "sId": 0,
                                                              "stype": 0}],
                                             "status": "",
                                             "spin_rtp": 0.0,
                                             "bundleSize": 0,
                                             "currentPlan": "LevelPlan78",
                                             "CurrentLevel": 49,
                                             "SpinStatus": "",
                                             "Coin_divise_Bet": 1386,
                                             "coins_hold": -1000.0,
                                             "netDuration": 0.116943359,
                                             "requestTime": 0.116943359,
                                             "url": None,
                                             "http_cost_time": 3.6263465881347656,
                                             "increaseCoins": 0.0,
                                             "LoginDays": 1,
                                             "spintype": 0, "VIP": 0,
                                             "IsOutofCoin": 0,
                                             "UserSegment": "e"}},
                         "time": 1637046869581, "last_pay_interval": 18947,
                         "device.model": "iPhone8,4"},
                "log_type": "client_report",
                "max_bet": 20000, "total_pay": 0.0, "user_tags": {}, "register_time": 1637044015959, "mid": self.mid,
                "active_day": 1, "versionCode": None}
        fields = {"app_id": self.app_id, "message_type": "SpinClicked", "mid": self.mid, "version": "7.6.0",
                  "sub_type": "Club", "data": json.dumps(data)}
        m_redis.xadd_stream(fields, stream_name=stream_name)

    def purchase(self):
        stream_name = 'slots:server_event'
        data = {"SDKVersion": 0, "total_pay": 0.99, "user_tags": {}, "m_pay": 0.99, "register_time": 1637829378755,
                "app_id": self.app_id,
                "mid": self.mid, "bet_plan": "open_step_a3", "active_day": 1,
                "device": {"locale": "", "device_type": "ios", "timezone": 28800, "app_version": "6.4.0"},
                "versionCode": 0,
                "log_time": "2021-11-25T08:42:02.151Z",
                "data": {"last_pay_interval": 0, "name": "CoinPurchaseSucceeded",
                         "extra": {"id": 51,
                                   "event": {"assetData": "test buy", "IsClub": "0",
                                             "increaseCoins": 6000000,
                                             "7dpurchase": 100.979996,
                                             "UserID": "18754623-EF09-593A-8141-E6416A87CBDF",
                                             "increaseVipPoint": 10000,
                                             "VIPTotalPoint": 100,
                                             "lastpaytime": "00:05:36",
                                             "CurrentBalance": 6151700,
                                             "CurrentBetNum": None, "LoginDays": 1,
                                             "orderid": "order1637829734461",
                                             "subSourceType": "test", "buyPeriod": 390,
                                             "oldBalance": 151700, "CurrentMachine": "",
                                             "tourGameId": "", "TotalLoginDays": 1,
                                             "ServerBetReceived": True,
                                             "DefaultMultipler": 4, "promotionAdd": 0,
                                             "VIP": 0, "CurrentBet": 100,
                                             "availablespin": 1517, "vipMultiplier": 1,
                                             "tourGameRank": "",
                                             "isDataFromServer": "True", "Spin": 0,
                                             "buffAdd": 0, "sourceType": -1,
                                             "BaseCoins": 1500000,
                                             "appInstallTime": "1970-01-01-00-00",
                                             "pid": "com.wisdomnetwork.citylucky.pid.coinspack.tier6",
                                             "price": 99.99, "promotionMultiplier": 1,
                                             "currentPlan": "LevelPlan10",
                                             "skuName": "shop_99_99",
                                             "report_data": {"apiv": 1,
                                                             "language": "Chinese",
                                                             "gdpr_status": "2",
                                                             "device_model": "MacBookPro16,2",
                                                             "ip": "103.126.24.102",
                                                             "time_zone": 28800,
                                                             "country_source": "setting",
                                                             "source": "client",
                                                             "app_version_code": 0,
                                                             "device_band": "MacBookPro16,2",
                                                             "app_bundle": "com.wisdomnetwork.citylucky"},
                                             "ActualDiscount": 4, "prefabname": "",
                                             "PurchaseReportFB": True,
                                             "CurrentLevel": 1,
                                             "dealInfo": "1637829734461:order1637829734461:shop_99_99:com.wisdomnetwork.citylucky.pid.coinspack.tier6:2:6000000:-3004:-1:-1:test:99.99:",
                                             "FBID": "", "RewardList": "",
                                             "7dfavoritesku": "extra_1_0_99,shop_99_99,",
                                             "PurchaseAfEventName": "af_purchase",
                                             "privacyType": "CCPA",
                                             "CurLeaderboardRank": -1,
                                             "levelMultiplier": 1, "canCollectData": True,
                                             "UserSegment": "e"}}, "time": 1637829734489,
                         "last_pay_time": 1637829418264, "device.model": "MacBookPro16,2"},
                "log_type": "client_report"}
        fields = {"app_id": self.app_id, "message_type": "CoinPurchaseSucceeded", "mid": self.mid, "version": "7.6.0",
                  "data": json.dumps(data)}
        m_redis.xadd_stream(fields, stream_name=stream_name)

    def world_event(self):
        pass
