# -*- coding:utf-8 -*-
from rest_framework import serializers

from courseSystem.models import Course


class CourseSerializer(serializers.ModelSerializer):
    course = serializers.ReadOnlyField(source='Course.name')
    students = serializers.SerializerMethodField()
    teacher = serializers.SerializerMethodField()

    def get_students(self, obj):
        # 这里的obj是Course模型的实例
        return obj.students.count()

    def get_teacher(self, obj):
        # 获取与课程相关联的教师列表，并返回他们的username
        teachers = obj.teacher.all()

        return [{'username': teacher.username, 'id': teacher.id} for teacher in teachers]

    class Meta:
        model = Course
        fields = '__all__'
