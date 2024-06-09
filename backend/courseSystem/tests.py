# # from django.test import TestCase
#
# # Create your tests here.
# from datetime import datetime, timedelta
#
# # 获取当前日期
# today = datetime.today()
#
# # 确定本周的第一天是星期几
# # 可以通过today.weekday()获取当前星期几，周一为0，周二为1，依此类推
# # 需要将星期天作为一周的第一天，因此调整计算方式
# if today.weekday() == 6:  # 如果今天是星期天，则本周第一天为下一周的星期一
#     start_day = today + timedelta(days=1)
# else:
#     start_day = today - timedelta(days=today.weekday())
#
# # 计算本周的最后一天，即本周的星期六
# end_day = start_day + timedelta(days=6)
#
# # 格式化日期输出
# start_day_formatted = start_day.strftime('%Y-%m-%d')
# end_day_formatted = end_day.strftime('%Y-%m-%d')
#
# print(f"本周开始日期：{start_day_formatted}")
# print(f"本周结束日期：{end_day_formatted}")
#
# from datetime import datetime, timedelta
#
#
# def getweek_start_and_end(start_on_sunday=True):
#     """
#     返回本周的开始日期和结束日期。
#
#     参数：
#     start_on_sunday -- 布尔值，指定是否从星期天开始计算（默认值：True）
#
#     返回值：
#     一个列表，包含本周的开始日期和结束日期（格式为datetime对象）
#     """
#     today = datetime.today()
#     start_day = today - timedelta(days=today.weekday() + (not start_on_sunday))
#     end_day = start_day + timedelta(days=6)
#     return [start_day, end_day]
#
#
# # 示例用法
# start_date, end_date = getweek_start_and_end(start_on_sunday=True)
# print(f"本周开始日期：{start_date.strftime('%Y-%m-%d')}")
# print(f"本周结束日期：{end_date.strftime('%Y-%m-%d')}")

import bcrypt

# 要加密的密码
password = "123456"

# 生成盐并创建 bcrypt 哈希
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

print(hashed_password.decode('utf-8'))  # 打印 base64 编码的哈希值