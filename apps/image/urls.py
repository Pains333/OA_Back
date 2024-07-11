# 名字：Pains
# 时间：2024/7/4 17:54
from django.urls import path
from .views import ImageListView

app_name = 'image'

urlpatterns = [
    path('upload', ImageListView.as_view(), name="uploadImage"),
]