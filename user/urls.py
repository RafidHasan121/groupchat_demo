from django.urls import path
from .views import *

urlpatterns = [
    path("", landing, name="landing"),
    path("login/", login_page, name="login"),
]
