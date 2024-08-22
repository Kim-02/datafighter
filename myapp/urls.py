# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_view, name='my_view'),
    path('test_view/', views.test_view, name='test_view'),
]
