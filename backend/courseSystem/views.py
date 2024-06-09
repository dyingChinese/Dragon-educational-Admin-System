# -*- coding:utf-8 -*-
# Create your views here.
from django.core.cache import cache
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from common.utils import CommonPagination
from courseSystem.handle import APIResponse
from courseSystem.models import Course
from courseSystem.serializers import CourseSerializer


# Create your views here.
# 查看公共课表
@api_view(['GET'])
def get_course_schedule(request: WSGIRequest):
    aclass = request.GET.get('class', None)
    startOnSunday = (request.GET.get('Sunday', True) == 'True' or request.GET.get('Sunday', True) == 'true')

    # 构造查询条件
    query_set = Course.objects.all()
    if aclass:
        query_set = query_set.filter(class_name=aclass)
    # 执行查询并转换为JSON格式
    serializer = CourseSerializer(query_set, many=True)
    # 返回JSON响应
    return APIResponse(code=200200, msg='获取课程列表成功', data=serializer.data)



