# -*- coding:utf-8 -*-
import datetime
import locale
import platform
from multiprocessing import cpu_count

import django
import psutil


pyVersion = platform.python_version()
osBuild = platform.architecture()
node = platform.node()
pf = platform.platform()
processor = platform.processor()
pyComp = platform.python_compiler()
osName = platform.system()
memory = psutil.virtual_memory()

print(f'''
    ==================================================
    ================     学生管理系统     ==============
    ==================================================
    - 操作系统: {osName + " " + osBuild[0]}
    - python version: {pyVersion}
    - node: ${node}
    - 操作系统版本: {pf}
    - 处理器: {processor}
    - cpuCount: {cpu_count()}
    - Python编译器: {pyComp}
    - CPU运行占用: {round((psutil.cpu_percent(1)), 2)}
    - 内存总数: {round((float(memory.total) / 1024 / 1024 / 1024), 2)}
    - 已用内存数: {round((float(memory.used) / 1024 / 1024 / 1024), 2)}
    - 系统语言: {locale.getdefaultlocale()}
    - Django 版本: {django.get_version()}
    ============================= {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
''')
