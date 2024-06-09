from django.db import models

from common.models import User


# Create your models here.
# 课程表
class Course(models.Model):
    id = models.BigAutoField(primary_key=True)  # 用户唯一标识
    name = models.CharField(max_length=100, unique=True)  # 课程的名称
    description = models.TextField()  # 课程的描述，可以存储较长的文本
    credits = models.IntegerField()  # 课程的学分，使用IntegerField
    teacher = models.ManyToManyField(User, related_name='teacher')  # 课程的教师，通常是一个User模型的实例，这里使用ForeignKey关联
    location = models.CharField(max_length=255)  # 课程上课的地点，使用CharField存储地点信息
    time = models.DateTimeField()  # 课程的上课时间，使用DateTimeField存储时间信息
    type = models.CharField(max_length=50)  # 课程的类型，可以使用CharField存储类型名称
    students = models.ManyToManyField(User, related_name='students')  # 课程的入学者，可以使用ManyToManyField与Student模型相关联
    created_at = models.DateTimeField(auto_now_add=True)  # 课程创建的时间，自动生成，使用AutoNowAddField
    official_code = models.CharField(max_length=70, null=True)  # 课程官方代号，可以使用CharField存储

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name
        db_table = "course"
