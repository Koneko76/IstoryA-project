from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    # url(r'^$', views.index),
    path(r'^$', views.index, name="index"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
]