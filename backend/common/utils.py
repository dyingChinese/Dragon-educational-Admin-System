# -*- coding:utf-8 -*-
import datetime
import hashlib
import random
import string

from rest_framework.pagination import PageNumberPagination


def md5value(key):
    input_name = hashlib.md5()
    input_name.update(key.encode("utf-8"))
    md5str = (input_name.hexdigest()).lower()
    print('计算md5:', md5str)
    return md5str


def dict_fetchall(cursor):  # cursor是执行sql_str后的记录，作入参
    columns = [col[0] for col in cursor.description]  # 得到域的名字col[0]，组成List
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


def get_ip(request):
    """
    获取请求者的IP信息
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_ua(request):
    """
    获取请求者的IP信息
    """
    ua = request.META.get('HTTP_USER_AGENT')
    return ua[0:200]


def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def getWeekDays():
    """
    获取近一周的日期
    """
    week_days = []
    now = datetime.datetime.now()
    for i in range(7):
        day = now - datetime.timedelta(days=i)
        week_days.append(day.strftime('%Y-%m-%d %H:%M:%S.%f')[:10])
    week_days.reverse()  # 逆序
    return week_days


def get_monday():
    """
    获取本周周一日期
    """
    now = datetime.datetime.now()
    monday = now - datetime.timedelta(now.weekday())
    return monday.strftime('%Y-%m-%d %H:%M:%S.%f')[:10]


def getweek_start_and_end(start_on_sunday=True):
    """
    返回本周的开始日期和结束日期。

    参数：
    start_on_sunday -- 布尔值，指定是否从星期天开始计算（默认值：True）

    返回值：
    一个列表，包含本周的开始日期和结束日期（格式为datetime对象）
    """
    today = datetime.datetime.today()
    start_day = today - datetime.timedelta(days=today.weekday() + (not start_on_sunday))
    end_day = start_day + datetime.timedelta(days=6)
    return [start_day, end_day]


def generate_es_date_check_code(random_string, date_str):
    # 将日期后四位与随机字符串拼接
    combined_str = date_str + random_string
    # 计算MD5加密后的后7位
    md5_result = hashlib.md5(combined_str.encode()).hexdigest()[-7:]
    return md5_result


def generate_random_nickname():
    # 获取当前日期
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    # 生成8个随机字符
    random_string = generate_random_string(8)
    # 生成校验码
    final_code = generate_es_date_check_code(random_string, date_str)
    return f"es_{random_string}_{date_str}_{final_code}"


class CommonPagination(PageNumberPagination):
    page_size = 70
    page_size_query_param = 'pageSize'
    max_page_size = 300
    currentPage = 1

    def get_paginated_response(self, data, pageSize=70, currentPage=1):
        # print('pageSize:', pageSize, 'currentPage:', currentPage)
        if type(pageSize) == str:
            pageSize = int(pageSize)

        if type(currentPage) == str:
            currentPage = int(currentPage)

        return {
            'total': self.page.paginator.count,
            'pageSize': pageSize or self.page_size,
            'currentPage': currentPage or self.currentPage,
            'records': data
        }
