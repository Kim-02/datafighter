# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_view, name='my_view'),
    path('student_UI_view/', views.student_UI_view, name='student_UI_view'),
]
