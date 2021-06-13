from django.urls import path
from . import views

urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('register', views.Register.as_view(), name='register'),
    path('logout', views.logout, name='logout'),
    path('', views.emails_received, name='emails_received'),
    path('send-email', views.send_email, name='send_email'),
    path('sent', views.emails_sent, name='emails_sent'),
    path('delete', views.delete, name='delete'),
    path('reply', views.reply_email, name='reply'),
    path('forward', views.forward_email, name='forward'),
]    
