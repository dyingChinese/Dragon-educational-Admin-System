# 测试账号

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