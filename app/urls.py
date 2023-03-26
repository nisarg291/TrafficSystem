from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path('',views.login,name="login"),
    path('home',views.home,name="home"),
    path('userLogin',views.userLogin,name="UserLogin"),
    path('SocietyDetails',views.societyDetails,name="SocietyDetails"),
    path('AvailableParkings',views.availableParkings,name="AvailableParkings"),
    path('parking',views.parking,name="parking"),
    path('register',views.register,name="register"),
]
