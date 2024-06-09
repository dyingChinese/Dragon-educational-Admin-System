# -*- coding:utf-8 -*-
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from common.models import OpLog, LoginLog, User, Dormitory, UserSubTablesTEA, UserSubTableSTU


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class DormitorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dormitory
        fields = '__all__'
        # exclude = ['warden']  # 排除这些字段


class DormitoryStaticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dormitory
        fields = '__all__'
        # exclude = ['warden']  # 排除这些字段


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']


class LoginLogSerializer(serializers.ModelSerializer):
    log_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = LoginLog
        fields = '__all__'


class OpLogSerializer(serializers.ModelSerializer):
    re_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = OpLog
        fields = '__all__'


class UserTeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubTablesTEA
        # exclude = ['password']  # 排除这些字段
        fields = '__all__'
    # def get_sub_tables_tea(self, obj):
    #     print(f'obj {obj}')
    #     return User.objects.get(nickname=obj)


class UserStuSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubTableSTU
        # exclude = ['password']  # 排除这些字段
        fields = '__all__'

class CombinedSerializer(serializers.ModelSerializer):
    usersubtablestea = UserTeaSerializer()
    usersubtablestu = UserStuSerializer()
    groups = GroupSerializer(many=True)
    user_permissions = PermissionSerializer(many=True)
    dormitory = DormitorySerializer(read_only=True)

    class Meta:
        model = User
        exclude = ['password']  # 排除这些字段
    # def to_representation(self, instance):
    #     # 根据你的查询结果，你可以在这里自定义如何从实例中提取数据
    #     # 例如，如果 instance 是一个包含 User 和 UserTea 字段的字典：
    #     return {
    #         'id': instance['id'],
    #         'nickname': instance['nickname'],
    #         'username': instance['username'],
    #
    #         # ... 其他 UserTea 表的字段 ...
    #     }


class UserSerializer(serializers.ModelSerializer):
    serializers.ReadOnlyField(source='User.nickname')
    # 使用ManyRelatedField来处理多对多关系，指定关联的模型和子关系序列化器
    groups = serializers.ManyRelatedField(
        child_relation=GroupSerializer()  # 子关系序列化器
    )
    # groups = serializers.SerializerMethodField(read_only=True)
    user_permissions = serializers.ManyRelatedField(
        child_relation=PermissionSerializer()
        # 子关系序列化器
    )

    dormitory = DormitorySerializer(read_only=True)

    class Meta:
        model = User
        # fields = '__all__'  # 或者列出你想包含的字段列表
        exclude = ['password']  # 排除这些字段


class AclassRoomSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()
    average = serializers.DecimalField(max_digits=5, decimal_places=2)
    id = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    def get_id(self, obj):
        # 这里可以添加逻辑来生成或获取唯一标识符
        return obj.get('id', None)

    def get_duration(self, obj):
        return 4

    class Meta:
        model = UserSubTableSTU
        fields = ('id', 'institute', 'domain', 'grade', 'aclass', 'count', 'average', 'duration')
