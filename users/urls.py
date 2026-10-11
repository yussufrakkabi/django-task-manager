from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import login_view
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    
    
]