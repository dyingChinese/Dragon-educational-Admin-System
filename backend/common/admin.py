from django.contrib import admin

from common.models import User, UserSubTablesTEA, UserSubTableSTU, Dormitory

# Register your models here.
admin.site.register(User)
admin.site.register(UserSubTablesTEA)
admin.site.register(UserSubTableSTU)
admin.site.register(Dormitory)
