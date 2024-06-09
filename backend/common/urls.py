from django.urls import path

from common.views import UserInfoView

urlpatterns = [
    path('user/', UserInfoView.as_view())
]
