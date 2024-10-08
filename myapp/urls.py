# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_view, name='my_view'),
    path('student_UI_view/', views.student_UI_view, name='student_UI_view'),
    path('run_function/', views.run_function, name='run_function'),
    path('student_UI_view/refuse_page_view', views.refuse_page_view, name='refuse_page_view'),
    path('test_view/', views.test_view, name='test_view'),
    path('student_UI_view/change_info_view', views.change_info_view, name='change_info_view'),
    path('student_UI_view/recomend_page_view', views.recomend_page_view, name='recomend_page_view'),
    path('student_UI_view/change_simulation_view', views.change_simulation_view, name='change_simulation_view'),
]
