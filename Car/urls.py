from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('page1/', views.page1),
    path('page2/', views.page2),
]