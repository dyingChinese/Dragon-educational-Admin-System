# -*- coding:utf-8 -*-
from django.contrib.auth.models import AbstractUser, UserManager, Group, Permission
from django.db import models

from common.utils import generate_random_nickname


# 用户表
class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女')
    )  # 性别选择
    ROLE_CHOICES = (
        ('0', '管理员'),
        ('1', '普通用户')
    )  # 用户角色选择
    STATUS_CHOICES = (
        (-3, '待激活'),
        (-2, '异常'),
        (-1, '注销'),
        (0, '正常'),
        (1, '封号'),
    )  # 用户状态选择
    POLITICS_CHOICES = [
        ('群众', '群众'),
        ('团员', '团员'),
        ('党员', '党员'),
        ('预备党员', '预备党员'),
        ('共青团员', '共青团员'),
        ('无党派人士', '无党派人士'),
        ('民主党派', '民主党派'),
        ('宗教', '宗教'),
        ('其他', '其他'),
    ]  # 政治面貌选择
    objects = UserManager()
    id = models.BigAutoField(primary_key=True)  # 用户唯一标识
    username = models.CharField(max_length=50, null=True)  # 用户名
    password = models.CharField(max_length=516, null=True)  # 密码（应加密存储）
    role = models.CharField(max_length=50, blank=True, null=True)  # 用户角色，可以为空
    status = models.IntegerField(default=-3, choices=STATUS_CHOICES)  # 用户状态
    nickname = models.CharField(blank=False, null=False, max_length=40, unique=True,
                                default=generate_random_nickname())  # 昵称
    avatar = models.FileField(upload_to='avatar/', null=True)  # 头像
    mobile = models.CharField(max_length=13, blank=True, null=True)  # 手机号码
    email = models.CharField(max_length=70, blank=True, null=True)  # 电子邮箱
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)  # 用户性别
    description = models.TextField(max_length=200, null=True)  # 用户描述
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间，自动设置为当前时间
    official_id = models.CharField(max_length=70, null=True)  # 身份证号
    last_update_time = models.DateTimeField(auto_now=True, null=True)  # 最后更新时间，自动设置为当前时间
    political_affiliation = models.CharField(max_length=70, choices=POLITICS_CHOICES, null=True, default='群众')  # 政治面貌
    ethnicity = models.CharField(max_length=20, null=True)  # 民族
    groups = models.ManyToManyField(Group, related_name='user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions', blank=True)
    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = []
    list_display = ['id', 'nickname', 'username', 'mobile', 'gender', 'ethnicity']
    list_display_links = ('id', 'nickname', 'ethnicity')

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        db_table = "user"


# 学生附表
class UserSubTableSTU(models.Model):
    objects = models.Manager()
    id = models.OneToOneField(User, on_delete=models.CASCADE,
                              primary_key=True)  # 外键，关联到 User 模型的 id 字段。当 User 对象被删除时，相关的 UserSubTableSTU 对象也会被级联删除。
    institute = models.CharField(max_length=50, null=False)  # 学院名称，不允许为空。
    grade = models.CharField(max_length=50, null=False)  # 年级，不允许为空。
    domain = models.CharField(max_length=50, null=False)  # 专业领域，不允许为空。
    aclass = models.CharField(max_length=50, null=False)  # 班级，不允许为空。
    duration = models.IntegerField(default=4)  # 学制 四年, 五年, 三年
    enrollment_date = models.CharField(max_length=50, null=True)  # 入学年份，可以为空。
    graduation_time = models.CharField(max_length=50, null=True)  # 毕业年份，可以为空。
    grade_point = models.FloatField(null=True, default=0.0)  # 学分绩点
    graduation = models.CharField(max_length=200, null=True)  # 毕业去向

    class Meta:
        verbose_name = "用户学生附表"
        verbose_name_plural = verbose_name
        db_table = "user_subTable_STU"


# 教师附表
class UserSubTablesTEA(models.Model):
    objects = models.Manager()
    id = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)  # 教师职称
    department = models.CharField(max_length=100, blank=True, null=True)  # 所属部门
    position = models.CharField(max_length=100, blank=True, null=True)  # 职位
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # 联系电话
    email = models.EmailField(blank=True, null=True)  # 电子邮件地址
    office_location = models.CharField(max_length=200, blank=True, null=True)  # 办公室位置
    research_interests = models.TextField(blank=True, null=True)  # 研究兴趣

    class Meta:
        verbose_name = "用户教师附表"
        verbose_name_plural = verbose_name
        db_table = "user_subTable_TEA"


# 宿舍
class Dormitory(models.Model):
    objects = models.Manager()
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, unique=True)  # 用户id
    user_name = models.CharField(max_length=70, null=True)  # 用户姓名
    room_number = models.IntegerField()  # 房间号
    capacity = models.IntegerField()  # 宿舍的容量
    gender_allowed = models.CharField(max_length=10)  # 宿舍允许的性别，如男性、女性或混合。
    address = models.TextField()  # 宿舍地址
    emergency_contact = models.CharField(max_length=70, null=True)  # 紧急联系人
    emergency_contact_phone = models.CharField(max_length=20, null=True)  # 紧急联系人号码
    health = models.CharField(max_length=70, null=True, default='良好')  # 健康
    warden = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='responsible')  # 管理员
    warden_name = models.CharField(max_length=70, null=True)  # 管理员姓名
    list_display = ['id', 'nickname', 'room_number', 'capacity', 'address', 'health', 'warden']

    class Meta:
        verbose_name = "宿舍"
        verbose_name_plural = verbose_name
        db_table = "dormitory"

    def __str__(self):
        return self.id.nickname


# 角色
class Role(models.Model):
    STATUS_CHOICES = (
        (-2, '异常'),
        (0, '正常'),
        (1, '封禁'),
    )  # 用户状态选择
    objects = models.Manager()
    id = models.BigAutoField(primary_key=True)  # 用户唯一标识
    role_name = models.CharField(max_length=70, null=False)  # 角色名
    parent_role_id = models.IntegerField(null=None, default=-1)  # 父角色
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name
        db_table = "role"

    def __str__(self):
        return self.role_name


# 登录日志
class LoginLog(models.Model):
    objects = models.Manager()
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    ip = models.CharField(max_length=100, blank=True, null=True)
    ua = models.CharField(max_length=200, blank=True, null=True)
    log_time = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "登录日志"
        verbose_name_plural = verbose_name
        db_table = "login_log"


class OpLog(models.Model):
    objects = models.Manager()
    id = models.BigAutoField(primary_key=True)
    re_ip = models.CharField(max_length=100, blank=True, null=True)
    re_time = models.DateTimeField(auto_now_add=True, null=True)
    re_url = models.CharField(max_length=200, blank=True, null=True)
    re_method = models.CharField(max_length=10, blank=True, null=True)
    re_content = models.CharField(max_length=200, blank=True, null=True)
    access_time = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = "操作日志"
        verbose_name_plural = verbose_name
        db_table = "op_log"
