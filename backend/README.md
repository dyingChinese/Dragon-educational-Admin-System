## 后端运行

> | 项目创建时间 2024年6月9日

### 后端环境

- [x] Django 5.0.6
- [x] Django REST framework 3.15.1
- [x] Python 3.9.10
- [x] MySQL 8.0.27

### 后端运行

```bash
# 安装依赖
# 定位到backend目录
cd backend
pip install -r requirements.txt

# 修改配置文件
# 修改backend/backend/settings.py文件中的数据库配置为自己的数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'education', # 数据库名(确保数据库存在,没有则创建它)
        'USER': 'root', # 数据库用户名
        'PASSWORD': '123456', # 数据库密码
        'HOST': '127.0.0.1', # 数据库地址
        'PORT': '3306', # 数据库端口
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
        }
    }
}
# 运行SQL脚本
# 进入backend目录
cd backend
# 运行SQL脚本
mysql -u root -p < backend/initSQL/education.sql

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 运行
python manage.py runserver
```

# 常用测试账号

| 用户id | 账号     | 密码     | 角色    |
|------|--------|--------|-------|
| 9001 | dragon | 123456 | 超级管理员 |
| 112  | yunxiyan5   | 123456 | 教务管理员 |
| 119  | jiehongyu50   | 123456 | 宿舍管理员 |

```mysql
# 查询语句
select user_id, nickname, auth_group.name, user.is_active
from user
         join user_groups ug on user.id = ug.user_id
         join auth_group on ug.group_id = auth_group.id
where (auth_group.name = '教师' or auth_group.name = '宿舍管理员' or auth_group.name = '教务管理员')
  and user.is_active = 1
```