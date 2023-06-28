import pymysql

mysql_config_online = {
    "host": "bf-db-task-cluster.cluster-covszvog9bvq.us-east-1.rds.amazonaws.com",
    "password": "udRJnbYsOCyC",
    "db": "slots_go",
    "user": "040_dev_slotsgo",
    "port": 2306,
    "charset": "utf8mb4"
}

mysql_config_test = {
    "host": "172.16.10.250",
    "password": "task1802",
    "db": "slots_account",
    "user": "root",
    "port": 3306,
    "charset": "utf8mb4"
}

Mysql_config = mysql_config_test


class Mysql():
    def __init__(self):
        self.con = pymysql.connect(**Mysql_config)
        self.con.autocommit(1)

    def execute(self, sql, params, back=False):
        cursor = self.con.cursor()
        result = cursor.execute(sql, params)
        if back:
            result = cursor.fetchall()
        cursor.close()
        return result


mysql = Mysql()
