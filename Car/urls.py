from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('car/<int:pk>/rate/', views.rate_car, name='rate_car'),
    path('category/<int:brand_id>/', views.category, name='category'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('page1/', views.page1, name='page1'),
    path('page2/', views.page2, name='page2'),
    path('subscribe/', views.subscribe, name='subscribe'),
]