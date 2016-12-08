# coding=utf-8

# 代码修改自wangfei(wangfei@hanwang.com.cn)的C++代码
# 参见：http://download.csdn.net/source/1178

# ******************************************************************************
# 下面为阴历计算所需的数据,为节省存储空间,所以采用下面比较变态的存储方法.
# ******************************************************************************
# 数组g_lunar_month_day存入阴历1901年到2050年每年中的月天数信息，
# 阴历每月只能是29或30天，一年用12（或13）个二进制位表示，对应位为1表30天，否则为29天
g_lunar_month_day = [
    0x4ae0, 0xa570, 0x5268, 0xd260, 0xd950, 0x6aa8, 0x56a0, 0x9ad0, 0x4ae8, 0x4ae0,  # 1910
    0xa4d8, 0xa4d0, 0xd250, 0xd548, 0xb550, 0x56a0, 0x96d0, 0x95b0, 0x49b8, 0x49b0,  # 1920
    0xa4b0, 0xb258, 0x6a50, 0x6d40, 0xada8, 0x2b60, 0x9570, 0x4978, 0x4970, 0x64b0,  # 1930
    0xd4a0, 0xea50, 0x6d48, 0x5ad0, 0x2b60, 0x9370, 0x92e0, 0xc968, 0xc950, 0xd4a0,  # 1940
    0xda50, 0xb550, 0x56a0, 0xaad8, 0x25d0, 0x92d0, 0xc958, 0xa950, 0xb4a8, 0x6ca0,  # 1950
    0xb550, 0x55a8, 0x4da0, 0xa5b0, 0x52b8, 0x52b0, 0xa950, 0xe950, 0x6aa0, 0xad50,  # 1960
    0xab50, 0x4b60, 0xa570, 0xa570, 0x5260, 0xe930, 0xd950, 0x5aa8, 0x56a0, 0x96d0,  # 1970
    0x4ae8, 0x4ad0, 0xa4d0, 0xd268, 0xd250, 0xd528, 0xb540, 0xb6a0, 0x96d0, 0x95b0,  # 1980
    0x49b0, 0xa4b8, 0xa4b0, 0xb258, 0x6a50, 0x6d40, 0xada0, 0xab60, 0x9370, 0x4978,  # 1990
    0x4970, 0x64b0, 0x6a50, 0xea50, 0x6b28, 0x5ac0, 0xab60, 0x9368, 0x92e0, 0xc960,  # 2000
    0xd4a8, 0xd4a0, 0xda50, 0x5aa8, 0x56a0, 0xaad8, 0x25d0, 0x92d0, 0xc958, 0xa950,  # 2010
    0xb4a0, 0xb550, 0xb550, 0x55a8, 0x4ba0, 0xa5b0, 0x52b8, 0x52b0, 0xa930, 0x74a8,  # 2020
    0x6aa0, 0xad50, 0x4da8, 0x4b60, 0x9570, 0xa4e0, 0xd260, 0xe930, 0xd530, 0x5aa0,  # 2030
    0x6b50, 0x96d0, 0x4ae8, 0x4ad0, 0xa4d0, 0xd258, 0xd250, 0xd520, 0xdaa0, 0xb5a0,  # 2040
    0x56d0, 0x4ad8, 0x49b0, 0xa4b8, 0xa4b0, 0xaa50, 0xb528, 0x6d20, 0xada0, 0x55b0,  # 2050
]

# 数组gLanarMonth存放阴历1901年到2050年闰月的月份，如没有则为0，每字节存两年
g_lunar_month = [
    0x00, 0x50, 0x04, 0x00, 0x20,  # 1910
    0x60, 0x05, 0x00, 0x20, 0x70,  # 1920
    0x05, 0x00, 0x40, 0x02, 0x06,  # 1930
    0x00, 0x50, 0x03, 0x07, 0x00,  # 1940
    0x60, 0x04, 0x00, 0x20, 0x70,  # 1950
    0x05, 0x00, 0x30, 0x80, 0x06,  # 1960
    0x00, 0x40, 0x03, 0x07, 0x00,  # 1970
    0x50, 0x04, 0x08, 0x00, 0x60,  # 1980
    0x04, 0x0a, 0x00, 0x60, 0x05,  # 1990
    0x00, 0x30, 0x80, 0x05, 0x00,  # 2000
    0x40, 0x02, 0x07, 0x00, 0x50,  # 2010
    0x04, 0x09, 0x00, 0x60, 0x04,  # 2020
    0x00, 0x20, 0x60, 0x05, 0x00,  # 2030
    0x30, 0xb0, 0x06, 0x00, 0x50,  # 2040
    0x02, 0x07, 0x00, 0x50, 0x03  # 2050
]

# ==================================================================================

from datetime import date, datetime
from calendar import Calendar as Cal

START_YEAR = 1901




def get_leap_month(lunar_year):
    flag = g_lunar_month[(lunar_year - START_YEAR) / 2]
    if (lunar_year - START_YEAR) % 2:
        return flag & 0x0f
    else:
        return flag >> 4


def lunar_month_days(lunar_year, lunar_month):
    if (lunar_year < START_YEAR):
        return 30

    high, low = 0, 29
    iBit = 16 - lunar_month;

    if (lunar_month > get_leap_month(lunar_year) and get_leap_month(lunar_year)):
        iBit -= 1

    if (g_lunar_month_day[lunar_year - START_YEAR] & (1 << iBit)):
        low += 1

    if (lunar_month == get_leap_month(lunar_year)):
        if (g_lunar_month_day[lunar_year - START_YEAR] & (1 << (iBit - 1))):
            high = 30
        else:
            high = 29

    return (high, low)


def lunar_year_days(year):
    days = 0
    for i in range(1, 13):
        (high, low) = lunar_month_days(year, i)
        days += high
        days += low
    return days


def get_ludar_date(tm):
    tm = datetime(int(tm[0:4]), int(tm[4:6]), int(tm[6:8]))
    span_days = (tm - datetime(START_YEAR, 1, 1)).days

    # 阳历1901年2月19日为阴历1901年正月初一
    # 阳历1901年1月1日到2月19日共有49天
    if (span_days < 49):
        year = 1901 - 1
        if (span_days < 19):
            month = 11
            day = 11 + span_days
        else:
            month = 12
            day = span_days - 18
        return (year, month, day)

    # 下面从阴历1901年正月初一算起
    span_days -= 49
    year, month, day = START_YEAR, 1, 1
    # 计算年
    tmp = lunar_year_days(year)
    while span_days >= tmp:
        span_days -= tmp
        year += 1
        tmp = lunar_year_days(year)

    # 计算月
    (foo, tmp) = lunar_month_days(year, month)
    while span_days >= tmp:
        span_days -= tmp
        if (month == get_leap_month(year)):
            (tmp, foo) = lunar_month_days(year, month)
            if (span_days < tmp):
                return (0, 0, 0)
            span_days -= tmp
        month += 1
        (foo, tmp) = lunar_month_days(year, month)

    # 计算日
    day += span_days
    if len(str(month)) == 1:
        month = '0' + str(month)
    if len(str(day)) == 1:
        day = '0' + str(day)
    return str(year) + str(month) + str(day)


# 功能简单，只打印当月的
#('19900811')