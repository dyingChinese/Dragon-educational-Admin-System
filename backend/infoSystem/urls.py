from django.urls import path

from infoSystem.views import UserView, DormitoryView, OpLogView, LoginLogView, UserTeaView, AclassView, \
    get_institute_category, get_institute_static, UserStuView, CourseView, getDormitoryStatic, AdminView, \
    get_permissions, get_auth_group

urlpatterns = [
    # 全体用户信息
    path('user', UserView.as_view()),
    path('user/<int:parmaId>', UserView.as_view()),

    # 全体用户信息
    path('userStu', UserStuView.as_view()),
    path('userStu/<int:pk>', UserStuView.as_view()),

    # 教师信息
    path('userTea', UserTeaView.as_view()),
    path('userTea/<int:pk>', UserTeaView.as_view()),

    # 宿舍信息
    path('dormitory', DormitoryView.as_view()),
    path('dormitory/<int:pk>', DormitoryView.as_view()),
    path('dormitory/getDormitoryStatic', getDormitoryStatic),

    # 班级信息
    path('aclass', AclassView.as_view()),
    path('aclass/getInstitute', get_institute_category),

    # 课程信息
    path('course', CourseView.as_view()),
    path('course/<int:pk>', CourseView.as_view()),

    # 学院信息
    path('institute', get_institute_static),

    # 管理员信息
    path('admin/role', AdminView.as_view()),
    path('admin/permission', get_permissions),
    path('admin/role/<int:pk>', AdminView.as_view()),
    path('admin/roleName', get_auth_group),

    # 操作日志
    path('oplog', OpLogView.as_view()),
    path('oplog/<int:pk>', OpLogView.as_view()),

    # 登录日志
    path('LoginLog', LoginLogView.as_view()),
    path('LoginLog/<int:pk>', LoginLogView.as_view()),
]
