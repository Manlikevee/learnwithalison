from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path("courses/<str:course_id>/", views.course_detail, name="course_detail"),
    path('', views.dashboard, name='dashboard'),
]
