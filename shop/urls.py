from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('update_cart_quantity/<int:pk>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('order_success/<str:order_id>/', views.order_success, name='order_success'),
    path('return_request/<str:order_id>/', views.return_request, name='return_request'),
    path('search/', views.search, name='search'),
]