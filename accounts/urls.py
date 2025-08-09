from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verify/<str:token>/', views.verify_email, name='verify_email'),
    path('2fa/setup/', views.two_factor_setup, name='2fa_setup'),
    path('2fa/verify/', views.two_factor_verify, name='2fa_verify'),
    path('profile/', views.profile, name='profile'),
]