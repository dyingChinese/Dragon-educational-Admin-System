# -*- coding:utf-8 -*-
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from common.handle import APIResponse
from common.models import User
from common.serializers import UserSerializer


# 登录视图
class LoginView(APIView):
    def get(self, request, format=None):
        return render(request, template_name='loginView.html')

    def post(self, request, format=None):
        # 获取用户名和密码
        username = request.data.get('username')
        password = request.data.get('password')
        # 尝试认证用户
        user = authenticate(username=username, password=password)
        # 如果用户认证成功
        if user is not None:
            # 创建一个 refresh token
            refresh = RefreshToken.for_user(user)
            # 返回 token
            return APIResponse(code=200200, msg='认证成功', data={'refresh': str(refresh),
                                                                  'access': str(refresh.access_token)})
        else:
            # 如果认证失败，返回错误信息
            return APIResponse(code=400403, msg='认证失败')


# 用户信息视图
class UserInfoView(APIView):

    def get(self, request, format=None):
        # 获取当前登录的用户
        user = request.user
        if user.is_authenticated:
            # 序列化用户数据
            user = User.objects.filter(nickname=user.nickname).first()

            # user.user_permissions = user.get_group_permissions()
            serializer = UserSerializer(user)
            return APIResponse(code=200201, msg='查询用户信息成功', data=serializer.data)
        else:
            return APIResponse(code=400400, msg='查询用户信息失败')

    def patch(self, request, format=None):
        user = request.user
        if user.is_authenticated:

            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return APIResponse(code=200201, msg='修改用户信息成功', data=serializer.data)
            else:
                return APIResponse(code=400400, msg='查询用户信息失败')
        else:
            return APIResponse(code=400403, msg='修改用户信息失败')


@api_view(['POST'])
@csrf_exempt
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return APIResponse(code=200200, msg='认证成功', data={
            'userInfo': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)})
    else:
        return APIResponse(code=400403, msg='认证失败')



