from django.urls import path

from courseSystem.views.admin import SimplyCRUD
from courseSystem.views.user import views as UserView

urlpatterns = [
    path('getCourseSchedule/', UserView.get_course_schedule),
    path('courseSchedule/', SimplyCRUD.CourseView.as_view()),
]
