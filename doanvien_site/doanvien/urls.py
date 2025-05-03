from django.urls import path
from . import views

urlpatterns = [
    path('', views.member_list, name='member-list'),  # Trang chủ
    path("them-doan-vien/", views.add_member, name="add-member"),
]
