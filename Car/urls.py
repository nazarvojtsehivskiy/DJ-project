from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:brand_id>/', views.category, name='category'),
    path('page1/', views.page1, name='page1'),
    path('page2/', views.page2, name='page2'),
]