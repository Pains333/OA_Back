# 名字：Pains
# 时间：2024/7/10 10:53
from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('latest/inform', views.LatestInformView.as_view(), name='latest_inform'),
    path('latest/absent', views.LatestAbsentView.as_view(), name='latest_absent'),
    path('department/staff/count', views.DepartmentStaffCountView.as_view(), name='staff_count'),
]