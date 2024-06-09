from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Group, Permission
from django.core.cache import cache
from django.db import transaction
from django.db.models import Count, Avg
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from common.handle import APIResponse
from common.models import User, Dormitory, OpLog, LoginLog, UserSubTablesTEA, UserSubTableSTU
from common.serializers import UserSerializer, DormitorySerializer, OpLogSerializer, CombinedSerializer, \
    AclassRoomSerializer, UserTeaSerializer
from common.utils import CommonPagination
from courseSystem.models import Course
from courseSystem.serializers import CourseSerializer


@method_decorator(login_required, name='dispatch')
class UserView(APIView):
    key = 'UserInfoCache'  # 缓存名称
    pagination_class = CommonPagination()

    # @login_required
    # 定义一个函数来检查用户是否有相应权限
    def has_permission(self, user):
        # 教务管理员和宿舍管理员组
        return user.groups.filter(name='教务管理员') or user.groups.filter(name='宿舍管理员') or user.groups.filter(
            name='超级管理员')

    def get(self, request, **kwargs):
        # 检查是否有 'id' 在 URL 参数中
        # if parmaId in kwargs:
        #     # 获取指定 ID 的对象
        #     try:
        #         user = User.objects.get(pk=parmaId)
        #         serializer = UserSerializer(user)
        #         return APIResponse(code=200200, msg='查询用户数据成功', data=serializer.data)
        #     except User.DoesNotExist:
        #         return APIResponse(code=400404, msg='查询用户数据失败')
        serializer = None
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('pageSize', 70)
        cache_key = f"{self.key}:{page}:{limit}"
        # 如果指定了limit，则使用它，否则使用分页类的默认值
        if not limit:
            self.pagination_class.page_size = limit
        if not page:
            self.pagination_class.page_query_param = page
        # 这里实现查看功能
        data = cache.get(cache_key)
        if data is None:
            # 数据不存在于缓存中，进行数据库查询并存入缓存
            users = User.objects.all().order_by('id')
            page = self.pagination_class.paginate_queryset(queryset=users, request=request)
            serializer = UserSerializer(page, many=True)
            cache.set(cache_key, page, timeout=86400)  # 缓存一天，视情况调整
        else:
            serializer = UserSerializer(data, many=True)
        return APIResponse(code=200200, msg='查询用户数据成功',
                           data=self.pagination_class.get_paginated_response(serializer.data, limit, page))

    # @permission_required('User.add_user', raise_exception=False)
    def post(self, request, format=None):
        if not self.has_permission(user=request.user):
            return APIResponse(code=400403, msg='无权限')
        # 这里实现创建功能
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache_key_pattern = f"^{self.key}.+"
            cache.delete_pattern(cache_key_pattern)  # 清除匹配模式的缓存项
            return APIResponse(code=200200, msg='添加用户数据成功')
        return APIResponse(code=400400, msg='添加用户数据失败')

    # @permission_required('User.change_user', raise_exception=False)
    def put(self, request, pk, format=None):
        if not self.has_permission(user=request.user):
            return APIResponse(code=400403, msg='无权限')
        # 这里实现更新功能
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache_key_pattern = f"^{self.key}.+"
            cache.delete_pattern(cache_key_pattern)  # 清除匹配模式的缓存项
            return APIResponse(code=200200, msg='修改用户数据成功')
        return APIResponse(code=400400, msg='修改用户数据失败')

    @staff_member_required  # 超级管理员
    # @permission_required('User.delete_user', raise_exception=False)
    def delete(self, request, pk, format=None):
        # 这里实现删除功能
        if not self.has_permission(user=request.user):
            return APIResponse(code=400403, msg='无权限')
        user = get_object_or_404(User, pk=pk)
        user.delete()
        cache_key_pattern = f"^{self.key}.+"
        cache.delete_pattern(cache_key_pattern)  # 清除匹配模式的缓存项
        return APIResponse(code=200200, msg='删除用户数据成功')


@method_decorator(login_required, name='dispatch')
class DormitoryView(APIView):
    key = 'DormitoryInfoCache'  # 缓存名称
    pagination_class = CommonPagination()

    # 定义一个函数来检查用户是否有相应权限
    def has_permission(self, user):
        # 教务管理员和宿舍管理员组
        return user.groups.filter(name='宿舍管理员') or user.groups.filter(name='超级管理员')

    def get(self, request, format=None, **kwargs):
        # 检查是否有 'id' 在 URL 参数中
        # if 'id' in kwargs:
        #     # 获取指定 ID 的对象
        #     try:
        #         dormitory = Dormitory.objects.get(pk=kwargs['id'])
        #         serializer = DormitorySerializer(dormitory)
        #
        #         return APIResponse(code=200200, msg='查询宿舍数据成功', data=serializer.data)
        #     except Dormitory.DoesNotExist as e:
        #         return APIResponse(code=400404, msg='查询宿舍数据失败')
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('pageSize', 70)
        cache_key = f"{self.key}:{page}:{limit}"
        serializer = None
        # 如果指定了limit，则使用它，否则使用分页类的默认值
        if not limit:
            self.pagination_class.page_size = limit
        if not page:
            self.pagination_class.page_query_param = page
        # 这里实现查看功能
        data = cache.get(cache_key)
        if data is None:
            # 数据不存在于缓存中，进行数据库查询并存入缓存
            dormitories = Dormitory.objects.all().order_by('id')
            page = self.pagination_class.paginate_queryset(queryset=dormitories, request=request)
            serializer = DormitorySerializer(page, many=True)
            cache.set(cache_key, page, timeout=86400)
        else:
            serializer = DormitorySerializer(data, many=True)
        return APIResponse(code=200200, msg='查询宿舍数据成功',
                           data=self.pagination_class.get_paginated_response(serializer.data, limit, page))

    @permission_required('User.add_dormitory', raise_exception=False)
    def post(self, request, format=None):
        if not self.has_permission(user=request.user):
            return APIResponse(code=400403, msg='无权限')
        # 这里实现创建功能
        serializer = DormitorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache_key_pattern = f"^{self.key}.+"
            cache.delete_pattern(cache_key_pattern)  # 清除匹配模式的缓存项
            return APIResponse(code=200200, msg='添加宿舍数据成功')
        return APIResponse(code=400400, msg='添加宿舍数据失败')

    # @permission_required('Dormitory.change_dormitory', raise_exception=False)
    def put(self, request, pk):
        # if not self.has_permission(user=request.user):
        #     return APIResponse(code=400403, msg='无权限')
        # 这里实现更新功能
        try:
            dormitory = Dormitory.objects.get(pk=pk)
        except Dormitory.DoesNotExist:
            return APIResponse(code=400404, msg='宿舍数据不存在')
        serializer = DormitorySerializer(dormitory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.clear_cache()
            # cache_key_pattern = f"^{self.key}.+"
            # cache.delete_pattern(cache_key_pattern)  # 清除匹配模式的缓存项
            return APIResponse(code=200200, msg='修改宿舍数据成功')
        return APIResponse(code=400400, msg='修改宿舍数据失败')

    @staff_member_required  # 超级管理员
    def delete(self, request, pk, format=None):
        # 这里实现删除功能
        if not self.has_permission(user=request.user):
            return APIResponse(code=400403, msg='无权限')
        dormitory = get_object_or_404(Dormitory, pk=pk)
        dormitory.delete()
        cache_key_pattern = f"^{self.key}.+"
        cache.delete_pattern(cache_key_pattern)  # 清除匹配模式的缓存项
        return APIResponse(code=200200, msg='删除宿舍数据成功')

    def clear_cache(self):
        # cache.delete_pattern(self.key)  # 清除匹配模式的缓存项 LocMemCache Not support delete_pattern
        cache.clear()


@api_view(['GET', 'POST'])
@csrf_exempt
def getDormitoryStatic(request):
    pagination_class = CommonPagination()
    dormitory = Dormitory.objects.values('capacity', 'gender_allowed', 'health').annotate(
        capacityNum=Count('capacity'),
        healthNum=Count('health')).order_by('capacity')
    unique_id = 1
    for stat in dormitory:
        stat['id'] = unique_id
        unique_id += 1

    page = pagination_class.paginate_queryset(queryset=dormitory, request=request)

    return APIResponse(code=200200, msg='查询床位数据成功', data=pagination_class.get_paginated_response(page))


@method_decorator(login_required, name='dispatch')
class UserStuView(APIView):
    key = 'UserStuInfoCache'  # 缓存名称
    pagination_class = CommonPagination()
    serializer_class = CombinedSerializer
    queryset = UserSubTablesTEA.objects.all()

    def get_queryset(self):
        # 获取请求的用户组名为'教师'的用户信息
        return self.queryset.filter(id__groups__name='学生').order_by('id')

    def get(self, request, *args, **kwargs):
        serializer = None
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('pageSize', 70)
        cache_key = f"{self.key}:{page}:{limit}"
        if not limit:
            self.pagination_class.page_size = limit
        if not page:
            self.pagination_class.page_query_param = page
        data = cache.get(cache_key)
        if data is None:
            usersTeas = User.objects.all().filter(groups__name='学生').order_by('id')
            page = self.pagination_class.paginate_queryset(queryset=usersTeas, request=request)
            serializer = CombinedSerializer(page, many=True)
            cache.set(cache_key, page, timeout=86400)

        else:
            serializer = CombinedSerializer(data, many=True)
        return APIResponse(code=200200, msg='查询学生数据成功',
                           data=self.pagination_class.get_paginated_response(serializer.data, limit, page))

    @transaction.atomic
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist | UserSubTablesTEA.DoesNotExist:
            return APIResponse(code=400404, msg='用户数据不存在')
        now = datetime.now()
        userData = {
            'username': request.data.get('username'),
            'nickname': request.data.get('nickname'),
            'email': request.data.get('email'),
            'mobile': request.data.get('mobile'),
            'gender': request.data.get('gender'),
            'description': request.data.get('description'),
            'political_affiliation': request.data.get('political_affiliation'),
            'ethnicity': request.data.get('ethnicity'),
            # 'password': make_password(request.data.get('password'), hasher='bcrypt_sha256'),
            'official_id': request.data.get('official_id'),
            'last_update_time': now.strftime('%Y-%m-%dT%H:%M:%S')
        }
        serializer = UserSerializer(user, data=userData, partial=True)
        if serializer.is_valid():
            serializer.save()
            self.clear_cache()
            return APIResponse(code=200200, msg='修改用户数据成功')
        print(serializer.errors)
        return APIResponse(code=400400, msg='修改用户数据失败')

    def clear_cache(self):
        cache.clear()


@method_decorator(login_required, name='dispatch')
class UserTeaView(APIView):
    key = 'UserTeaInfoCache'  # 缓存名称
    pagination_class = CommonPagination()
    serializer_class = CombinedSerializer
    queryset = UserSubTablesTEA.objects.all()

    def get_queryset(self):
        # 获取请求的用户组名为'教师'的用户信息
        return self.queryset.filter(id__groups__name='教师').order_by('id')

    def get(self, request, *args, **kwargs):
        serializer = None
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('pageSize', 70)
        cache_key = f"{self.key}:{page}:{limit}"
        if not limit:
            self.pagination_class.page_size = limit
        if not page:
            self.pagination_class.page_query_param = page
        data = cache.get(cache_key)
        if data is None:
            usersTeas = User.objects.all().filter(groups__name='教师').order_by('id')
            page = self.pagination_class.paginate_queryset(queryset=usersTeas, request=request)
            serializer = CombinedSerializer(page, many=True)
            cache.set(cache_key, page, timeout=86400)
            # usersTeas = User.objects.all().filter(groups__name='教师').order_by('id')
            # usersTeas = User.objects.raw("""
            #         SELECT user.*, auth_group.name as role, ust.*
            #         FROM user
            #                  JOIN user_groups ON user.id = user_groups.user_id
            #                  JOIN auth_group ON user_groups.group_id = auth_group.id
            #                  join user_subtable_tea ust on user.id = ust.id_id
            #         WHERE auth_group.name = '教师';
            # """)

        else:
            serializer = CombinedSerializer(data, many=True)
        return APIResponse(code=200200, msg='查询教师数据成功',
                           data=self.pagination_class.get_paginated_response(serializer.data, limit, page))

    @transaction.atomic
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            userTea = UserSubTablesTEA.objects.get(pk=pk)
        except User.DoesNotExist | UserSubTablesTEA.DoesNotExist:
            return APIResponse(code=400404, msg='用户数据不存在')
        now = datetime.now()
        userData = {
            'username': request.data.get('username'),
            'nickname': request.data.get('nickname'),
            'email': request.data.get('email'),
            'mobile': request.data.get('mobile'),
            'gender': request.data.get('gender'),
            'description': request.data.get('description'),
            'political_affiliation': request.data.get('political_affiliation'),
            'ethnicity': request.data.get('ethnicity'),
            # 'password': make_password(request.data.get('password'), hasher='bcrypt_sha256'),
            'official_id': request.data.get('official_id'),
            'last_update_time': now.strftime('%Y-%m-%dT%H:%M:%S')
        }
        userSerializer = UserSerializer(user, data=userData, partial=True)
        userTeaSerializer = UserTeaSerializer(userTea, data=request.data.get('usersubtablestea'))
        if userSerializer.is_valid() and userTeaSerializer.is_valid():
            userSerializer.save()
            userTeaSerializer.save()
            self.clear_cache()
            return APIResponse(code=200200, msg='修改用户数据成功')
        return APIResponse(code=400400, msg='修改用户数据失败')

    def clear_cache(self):
        # cache.delete_pattern(self.key)  # 清除匹配模式的缓存项 LocMemCache Not support delete_pattern
        cache.clear()


@method_decorator(login_required, name='dispatch')
class AclassView(APIView):
    key = 'AClassInfoCache'  # 缓存名称
    pagination_class = CommonPagination()
    serializer_class = AclassRoomSerializer

    def get(self, request, *args, **kwargs):
        serializer = None
        keyword = request.query_params.get('keyword', None)
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('pageSize', 70)
        cache_key = f"{self.key}:{page}:{limit}:{keyword}"
        if not limit:
            self.pagination_class.page_size = limit
        if not page:
            self.pagination_class.page_query_param = page

        data = cache.get(cache_key)
        if data is None:
            if keyword and keyword != '全部学院':
                class_room = UserSubTableSTU.objects.filter(institute=keyword).values('institute', 'grade', 'domain',
                                                                                      'aclass').annotate(
                    count=Count('id'), average=Avg('grade_point')).order_by('institute', 'grade', 'domain', 'aclass')
            else:
                class_room = UserSubTableSTU.objects.values('institute', 'grade', 'domain', 'aclass').annotate(
                    count=Count('id'), average=Avg('grade_point')).order_by('institute', 'grade', 'domain', 'aclass')
            unique_id = 1
            for stat in class_room:
                stat['id'] = unique_id
                unique_id += 1

            page = self.pagination_class.paginate_queryset(queryset=class_room, request=request)
            serializer = AclassRoomSerializer(page, many=True)
            cache.set(cache_key, page, timeout=86400)
        else:
            serializer = AclassRoomSerializer(data, many=True)
        return APIResponse(code=200200, msg='查询班级数据成功',
                           data=self.pagination_class.get_paginated_response(serializer.data, limit, page))


@api_view(['GET', 'POST'])
@csrf_exempt
def get_institute_category(request):
    # class_room = UserSubTableSTU.objects.values('institute').distinct().order_by('institute')
    class_room = UserSubTableSTU.objects.values_list('institute', flat=True).distinct().order_by('institute')
    return APIResponse(code=200200, msg='查询学院数据成功', data=class_room)


@api_view(['GET', 'POST'])
@csrf_exempt
def get_institute_static(request):
    # class_room = UserSubTableSTU.objects.values('institute').distinct().order_by('institute')
    pagination_class = CommonPagination()
    class_room = UserSubTableSTU.objects.values('institute', ).annotate(
        domainCount=Count('domain'), stuNum=Count('id')
    ).order_by('institute')

    unique_id = 1
    for stat in class_room:
        stat['id'] = unique_id
        unique_id += 1

    page = pagination_class.paginate_queryset(queryset=class_room, request=request)
    return APIResponse(code=200200, msg='查询学院数据成功', data=pagination_class.get_paginated_response(page))


@method_decorator(login_required, name='dispatch')
class CourseView(APIView):
    key = 'CourseInfoCache'  # 缓存名称
    pagination_class = CommonPagination()

    # serializer_class =

    def get(self, request, *args, **kwargs):
        serializer = None
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('pageSize', 70)
        cache_key = f"{self.key}:{page}:{limit}"
        if not limit:
            self.pagination_class.page_size = limit
        if not page:
            self.pagination_class.page_query_param = page
        data = cache.get(cache_key)
        if data is None:
            course = Course.objects.all().order_by('id')
            page = self.pagination_class.paginate_queryset(queryset=course, request=request)
            serializer = CourseSerializer(page, many=True)
            cache.set(cache_key, page, timeout=86400)

        else:
            serializer = CourseSerializer(data, many=True)
        return APIResponse(code=200200, msg='查询课程数据成功',
                           data=self.pagination_class.get_paginated_response(serializer.data, limit, page))


@method_decorator(login_required, name='dispatch')
class OpLogView(APIView):
    key = 'OpLogInfoCache'  # 缓存名称
    pagination_class = CommonPagination()

    # 定义一个函数来检查用户是否有相应权限
    def has_permission(self, user):
        # 教务管理员和宿舍管理员组
        return user.groups.filter(name='超级管理员')

    # @login_required(login_url='/login/')
    def get(self, request, format=None, **kwargs):
        # 检查是否有 'id' 在 URL 参数中
        if 'id' in kwargs:
            # 获取指定 ID 的对象
            try:
                oplog = OpLog.objects.get(pk=kwargs['id'])
                serializer = OpLogSerializer(oplog)
                return APIResponse(code=200200, msg='查询操作日志数据成功', data=serializer.data)
            except (OpLog.DoesNotExist, exceptions.APIException, exceptions.NotFound) as e:

                return APIResponse(code=400404, msg='查询操作日志数据失败')

        page = request.query_params.get('page', 1)
        limit = request.query_params.get('PageSize', 70)
        cache_key = f"{self.key}:{request.query_params.get('page', 1)}:{request.query_params.get('page_size', self.pagination_class.page_size)}"
        # 如果指定了limit，则使用它，否则使用分页类的默认值
        if limit:
            self.pagination_class.page_size = limit
        if page:
            self.pagination_class.page_query_param = page
        # 这里实现查看功能
        data = cache.get(cache_key)
        if data is None:
            # 数据不存在于缓存中，进行数据库查询并存入缓存
            oplogs = OpLog.objects.all()
            page = self.pagination_class.paginate_queryset(queryset=oplogs, request=request)
            serializer = OpLogSerializer(page, many=True)
            cache.set(cache_key, serializer.data, timeout=86400)  # 缓存一天，视情况调整
        else:
            serializer = OpLogSerializer(data, many=True)
        return APIResponse(code=200200, msg='查询操作日志数据成功', data=serializer.data)

    @permission_required('User.add_oplog', raise_exception=False)
    def post(self, request, format=None):
        # 这里实现创建功能
        serializer = OpLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache_key_pattern = f"^{self.key}.+"
            cache.delete_pattern(cache_key_pattern)  # 清除匹配模式的缓存项
            return APIResponse(code=200200, msg='添加操作日志数据成功')
        return APIResponse(code=400400, msg='添加操作日志数据失败')

    @permission_required('User.change_oplog', raise_exception=False)
    def put(self, request, pk, format=None):
        # 这里实现更新功能
        oplog = get_object_or_404(OpLog, pk=pk)
        serializer = OpLogSerializer(oplog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache_key_pattern = f"^{self.key}.+"
            cache.delete_pattern(cache_key_pattern)  # 清除匹配模式的缓存项
            return APIResponse(code=200200, msg='修改操作日志数据成功')
        return APIResponse(code=400400, msg='修改操作日志数据失败')

    @staff_member_required  # 超级管理员
    @permission_required('User.delete_oplog', raise_exception=False)
    def delete(self, request, pk, format=None):
        # 这里实现删除功能
        oplog = get_object_or_404(OpLog, pk=pk)
        oplog.delete()
        cache_key_pattern = f"^{self.key}.+"
        cache.delete_pattern(cache_key_pattern)  # 清除匹配模式的缓存项
        return APIResponse(code=200200, msg='删除操作日志数据成功')


@method_decorator(login_required, name='dispatch')
class LoginLogView(APIView):
    key = 'LoginLogInfoCache'  # 缓存名称
    pagination_class = CommonPagination()

    # 定义一个函数来检查用户是否有相应权限
    def has_permission(self, user):
        # 教务管理员和宿舍管理员组
        return user.groups.filter(name='教务管理员') or user.groups.filter(name='宿舍管理员') or user.groups.filter(
            name='超级管理员')

    @login_required
    @permission_required('User.view_loginlog', raise_exception=False)
    def get(self, request, format=None, **kwargs):
        # 检查是否有 'id' 在 URL 参数中
        user = request.user
        if not self.has_permission(user=user):
            return APIResponse(code=400403, msg='无权限')
        if 'id' in kwargs:
            # 获取指定 ID 的对象
            try:
                loginlog = LoginLog.objects.get(pk=kwargs['id'])
                serializer = OpLogSerializer(loginlog)
                return APIResponse(code=200200, msg='查询登录日志数据成功', data=serializer.data)
            except LoginLog.DoesNotExist:
                return APIResponse(code=400404, msg='查询登录日志数据失败')

        page = request.query_params.get('page', 1)
        limit = request.query_params.get('PageSize', 70)
        cache_key = f"{self.key}:{request.query_params.get('page', 1)}:{request.query_params.get('page_size', self.pagination_class.page_size)}"
        # 如果指定了limit，则使用它，否则使用分页类的默认值
        if limit:
            self.pagination_class.page_size = limit
        if page:
            self.pagination_class.page_query_param = page
        # 这里实现查看功能
        data = cache.get(cache_key)
        if data is None:
            # 数据不存在于缓存中，进行数据库查询并存入缓存
            loginlogs = LoginLog.objects.all()
            page = self.pagination_class.paginate_queryset(queryset=loginlogs, request=request)
            serializer = OpLogSerializer(page, many=True)
            cache.set(cache_key, serializer.data, timeout=86400)  # 缓存一天，视情况调整
        else:
            serializer = OpLogSerializer(data, many=True)
        return APIResponse(code=200200, msg='查询登录日志数据成功', data=serializer.data)

    @permission_required('User.add_loginlog', raise_exception=False)
    def post(self, request, format=None):
        if not self.has_permission(user=request.user):
            return APIResponse(code=400403, msg='无权限')
        # 这里实现创建功能
        serializer = OpLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache_key_pattern = f"^{self.key}.+"
            cache.delete_pattern(cache_key_pattern)  # 清除匹配模式的缓存项
            return APIResponse(code=200200, msg='添加登录日志数据成功')
        return APIResponse(code=400400, msg='添加登录日志数据失败')

    @permission_required('User.change_loginlog', raise_exception=False)
    def put(self, request, pk, format=None):
        if not self.has_permission(user=request.user):
            return APIResponse(code=400403, msg='无权限')
        # 这里实现更新功能
        loginlog = get_object_or_404(LoginLog, pk=pk)
        serializer = OpLogSerializer(loginlog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache_key_pattern = f"^{self.key}.+"
            cache.delete_pattern(cache_key_pattern)  # 清除匹配模式的缓存项
            return APIResponse(code=200200, msg='修改登录日志数据成功')
        return APIResponse(code=400400, msg='修改登录日志数据失败')

    @staff_member_required  # 超级管理员
    @permission_required('User.delete_loginlog', raise_exception=False)
    def delete(self, request, pk, format=None):
        # 这里实现删除功能
        if not self.has_permission(user=request.user):
            return APIResponse(code=400403, msg='无权限')
        loginlog = get_object_or_404(LoginLog, pk=pk)
        loginlog.delete()
        cache_key_pattern = f"^{self.key}.+"
        cache.delete_pattern(cache_key_pattern)  # 清除匹配模式的缓存项
        return APIResponse(code=200200, msg='删除登录日志数据成功')


@api_view(['GET'])
def get_auth_group(request):
    user_groups = Group.objects.values().distinct().order_by('id')
    return APIResponse(code=200200, msg='查询用户组数据成功', data=list(user_groups))


class AdminView(APIView):
    key = 'AdminGroupCache'  # 缓存名称
    pagination_class = CommonPagination()
    serializer_class = UserSerializer

    def has_permission(self, req):
        # 替换 'group_name' 为您希望检查的组的名称
        return Group.objects.filter(name='超级管理员', user=req.user).exists()

    def get(self, request, *args, **kwargs):
        user = request.user

        page = request.query_params.get('page', 1)
        limit = request.query_params.get('pageSize', 70)
        keyword = request.query_params.get('name', '全部')

        if not limit:
            self.pagination_class.page_size = limit
        if not page:
            self.pagination_class.page_query_param = page

        if not user.groups.filter(name='超级管理员').exists():
            return APIResponse(code=400403, msg='无权限')

        if keyword and keyword == '全部':
            cache_key = f"{self.key}:{page}:{limit}"
            data = cache.get(cache_key)
            if data is not None:
                serializer = UserSerializer(data, many=True)
                return APIResponse(code=200200, msg='查询用户数据成功',
                                   data=self.pagination_class.get_paginated_response(serializer.data, limit, page))

            users = User.objects.all().order_by('id')
            page = self.pagination_class.paginate_queryset(queryset=users, request=request)
            serializer = UserSerializer(page, many=True)
            cache.set(cache_key, page, timeout=86400)
            return APIResponse(code=200200, msg='查询用户数据成功',
                               data=self.pagination_class.get_paginated_response(serializer.data, limit, page))

        if keyword and keyword != '全部':
            cache_key = f"{self.key}:{page}:{limit}:{keyword}"
            data = cache.get(cache_key)

            if data is not None:
                serializer = UserSerializer(data, many=True)
                return APIResponse(code=200200, msg='查询用户数据成功',
                                   data=self.pagination_class.get_paginated_response(serializer.data, limit, page))

            users_for_group = User.objects.filter(groups__name=keyword).all().distinct().order_by('id')

            page = self.pagination_class.paginate_queryset(queryset=users_for_group, request=request)
            serializer = UserSerializer(page, many=True)
            cache.set(cache_key, page, timeout=86400)
            return APIResponse(code=200200, msg='查询用户数据成功',
                               data=self.pagination_class.get_paginated_response(serializer.data, limit, page))
        # 如果有其他权限检查，可以在这里添加
        # if not self.has_permission(request):
        #     return APIResponse(code=400403, msg='无权限')
        # 获取所有用户的组名称
        user_groups = Group.objects.values().distinct().order_by('id')
        # 返回响应
        return APIResponse(code=200200, msg='查询用户组数据成功', data=list(user_groups))


@api_view(['GET'])
def get_permissions(request):
    # 获取用户的权限
    user = request.user
    keyword = request.query_params.get('group', 'total')
    if not user.groups.filter(name='超级管理员').exists():
        return APIResponse(code=400403, msg='无权限')
    if keyword and keyword != 'total':
        user_permissions = Permission.objects.filter(group__name=keyword).values().distinct().order_by('id')
        return APIResponse(code=200200, msg='查询用户权限数据成功', data=list(user_permissions))
    user_permissions = user.user_permissions.values().distinct().order_by('id')
    return APIResponse(code=200200, msg='查询用户权限数据成功', data=list(user_permissions))
