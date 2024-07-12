from django.contrib import admin
from django.urls import path, include
from accounts import views  # Import views from your accounts app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', views.home_view, name='home'),  
    path('chat/', views.chat_view, name='chat'),  # Add this line for the chat functionality
]