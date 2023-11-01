from django.contrib.auth import views as auth_views

from django.urls import path
from . import views




urlpatterns = [
    path("", views.HomePage, name="home"),
    path("upload/", views.Upload_Image, name="upload_reciept"),
    path("calculator/", views.Calculator, name="calculator"),
    # path("", views.HomePage, name="home"),


    # AUTH
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
]