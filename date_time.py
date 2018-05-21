# -*- coding:utf-8 -*-

import re
from datetime import datetime, timezone, timedelta
def to_timestamp(dt_str, tz_str):
    cday=datetime.strptime(dt_str,'%Y-%m-%d %H:%M:%S')   #转换时间信息（由字符提取时间）
    realutc=re.match(r'UTC([\+\-]?\d+):\d+',tz_str)     #正则获取时区数字
    hutc=realutc.group(1)
    tz_utc = timezone(timedelta(hours=int(hutc)))          #将时区设置给时间
    cday = cday.replace(tzinfo=tz_utc)

    return cday.timestamp()   #返回毫秒数


# 测试:
t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')
assert t1 == 1433121030.0, t1

t2 = to_timestamp('2015-5-31 16:10:30', 'UTC-09:00')
assert t2 == 1433121030.0, t2

print('ok')
