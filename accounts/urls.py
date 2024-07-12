from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.home_view, name='home'),
    path('chat/', views.chat_view, name='chat'),  # Add this line for the chat functionality
]