from rest_framework.views import APIView

from common.handle import APIResponse
from courseSystem.models import Course
from courseSystem.serializers import CourseSerializer


class CourseView(APIView):
    def get(self, request, format=None):
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

    # def post(self, request, format=None):