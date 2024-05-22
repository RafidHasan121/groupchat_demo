from django.urls import path
from .views import *

urlpatterns = [
    path("", landing, name="landing"),
    path("login/", login_page, name="login"),
    path("logout/", logout, name="logout"),
    path("invite/", invite, name="invite"),
]
