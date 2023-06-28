import time

current_time = time.gmtime()
hour = current_time.tm_hour
minute = 0
second = 0
current_times = time.mktime((current_time.tm_year, current_time.tm_mon, current_time.tm_mday, hour, minute, second,
                             current_time.tm_wday, current_time.tm_yday, current_time.tm_isdst))
b_current_time = time.mktime((current_time.tm_year + 1, current_time.tm_mon, current_time.tm_mday, hour, minute, second,
                              current_time.tm_wday, current_time.tm_yday, current_time.tm_isdst))


# utc凌晨0点
def today_time():
    current_time = time.gmtime()
    current_times = time.mktime((current_time.tm_year, current_time.tm_mon, current_time.tm_mday, 0, 0, 0,
                                 current_time.tm_wday, current_time.tm_yday, current_time.tm_isdst))
    return current_times


def tomorrow_time():
    current_time = time.gmtime()
    current_times = time.mktime((current_time.tm_year, current_time.tm_mon, current_time.tm_mday + 1, 0, 0, 0,
                                 current_time.tm_wday, current_time.tm_yday, current_time.tm_isdst))
    return current_times


def time_difference(year=0, mon=0, day=0, hour=0, minute=0, second=0):
    current_time = time.gmtime()
    current_times = time.mktime(
        (current_time.tm_year + year, current_time.tm_mon + mon, current_time.tm_mday + day, 0, 0, 0,
         current_time.tm_wday, current_time.tm_yday, current_time.tm_isdst))
    return int(current_times)
