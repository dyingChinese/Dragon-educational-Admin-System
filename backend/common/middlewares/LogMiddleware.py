# -*- coding:utf-8 -*-
import json
import time

from django.utils.deprecation import MiddlewareMixin

from common.serializers import OpLogSerializer
from common.utils import get_ip


class OpLogs(MiddlewareMixin):

    def __init__(self, *args):
        super(OpLogs, self).__init__(*args)

        self.start_time = None  # 开始时间
        self.end_time = None  # 响应时间
        self.data = {}  # dict数据

    def process_request(self, request):

        self.start_time = time.time()  # 开始时间

        re_ip = get_ip(request)
        re_method = request.method
        re_content = request.GET if re_method == 'GET' else request.POST
        if re_content:
            re_content = json.dumps(re_content)
        else:
            re_content = None

        self.data.update(
            {
                're_url': request.path,
                're_method': re_method,
                're_ip': re_ip,
                're_content': re_content,
            }
        )
        # print(self.data)

    def process_response(self, request, response):

        # 耗时毫秒/ms
        self.end_time = time.time()  # 响应时间
        access_time = self.end_time - self.start_time
        self.data['access_time'] = round(access_time * 1000)

        # 入库
        serializer = OpLogSerializer(data=self.data)
        if serializer.is_valid():
            serializer.save()

        return response
