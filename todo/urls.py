from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('',views.taskList, name='task'),
    path('delete/<int:pk>/', views.deleteTask, name='delete-task'),
    path('edit/<int:pk>/',views.editTask, name='edit-task'),
    path('export/',views.export_csv,name='export-csv'),
    path('login/', LoginView.as_view(template_name='todo/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/',views.register, name='register'),
]
