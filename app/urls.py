from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('',views.Login, name='Login'),
    path('Register/',views.Register, name='Register'),
    path('Home/',views.Home, name='Home'),
]
