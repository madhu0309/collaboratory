from django.urls import path, include
from .views import SignupPageView
from .views import HomePageView

app_name = "users"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("signup/", SignupPageView.as_view(), name="signup"),
]
