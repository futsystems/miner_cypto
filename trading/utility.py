#!/usr/bin/python
# -*- coding: utf-8 -*-


import pytz
import datetime
import time


def timestamp_to_datetime(timestamp):
    """
    timestamp UTC绑定，无论提供什么时区返回的时间是相同的，因此此处默认番位UTC时区时间
    :param timestamp:
    :return:
    """
    return datetime.datetime.fromtimestamp(timestamp, pytz.utc)


def datetime_to_timestamp(dt):
    """
    timetuple直接取年月日，失去时区信息，因此需要先转换成UTC时间
    :param time_str:
    :return:
    """
    return time.mktime(dt.astimezone(pytz.utc).timetuple())


def utc_now():
    """
    返回UTC当前时间
    :return:
    """
    return datetime.datetime.now().astimezone(pytz.utc)


def utc_today():
    dt = datetime.datetime.now().astimezone(pytz.utc)
    return datetime.datetime(dt.year, dt.month, dt.day, 23, 59, 59, 999999, tzinfo=pytz.utc)

def string_to_datetime(dt_str):
    """
    %Y-%m-%d %H:%M:%S.%f
    默认提供的时间为UTC时间
    :param dt_str:
    :return:
    """
    dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d")
    #此处获得dt为无时区，转换成其他时区时，默认使用本机时区
    return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, tzinfo=pytz.utc)


if __name__ == "__main__":
    dt = string_to_datetime('2021-01-01')
    ts = datetime_to_timestamp(dt)
    print(ts)
    dt = string_to_datetime('2021-09-21')
    ts = datetime_to_timestamp(dt)
    print(ts)
