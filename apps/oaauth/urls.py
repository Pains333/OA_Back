# 名字：Pains
# 时间：2024/6/18 18:08
from django.urls import path
from .views import LoginView, RestPwdView

app_name = 'oaauth'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('resetpwd', RestPwdView.as_view(), name='resetpwd'),
]