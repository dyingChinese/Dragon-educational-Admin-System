import datetime
import hashlib
import random
import string


def generate_check_digit(number):
    # 这里是一个简单的校验码生成方法，实际应用中可能需要更复杂的算法
    check_digit = (number * 9) % 10
    return str(check_digit)


def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_es_date_check_code(random_string, date_str):
    # 将日期后四位与随机字符串拼接
    combined_str = date_str + random_string
    # 计算MD5加密后的后7位
    md5_result = hashlib.md5(combined_str.encode()).hexdigest()[-7:]
    return md5_result


# 获取当前日期
date_str = datetime.datetime.now().strftime("%Y%m%d")
# 生成8个随机字符
random_string = generate_random_string(8)
# 生成校验码
final_code = generate_es_date_check_code(random_string, date_str)

# 输出最终的字符串
print(f"es_{random_string}_{date_str}_{final_code}")










