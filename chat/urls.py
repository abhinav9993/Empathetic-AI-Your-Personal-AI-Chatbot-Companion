# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [

    path('',views.home,name='home'),
    path('chat_response/', views.chat_response, name='chat_response'),
    path('register/',views.register, name='register'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name = 'logout'),
]
