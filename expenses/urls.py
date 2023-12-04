from django.contrib.auth import views as auth_views

from django.urls import path
from . import views




urlpatterns = [
    path("", views.HomePage, name="home"),
    path("upload/", views.Upload_Image, name="upload_reciept"),
    path("upload_confirmation/<str:pk>", views.Upload_Image_Confirmation, name="upload_confirmation"),
    path("cancel/<str:pk>", views.Cancel, name="cancel"),
    path("update/<str:pk>", views.Update, name="update"),
    path("view/<str:pk>", views.View, name="view"),
    path("delete/<str:pk>", views.Delete, name="delete"),
    # path("upload_confirmation/", views.Upload_Image_Confirmation, name="upload_confirmation"),
    # path("calculator/", views.Calculator, name="calculator"),
    path("expenses/", views.ManageUpload, name="expenses"),
    path("expenses-add/", views.AddExpenses, name="add-expenses"),
    path("report/", views.Report, name="report"),
    # path("", views.HomePage, name="home"),


    # AUTH
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
]