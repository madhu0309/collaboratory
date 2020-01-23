from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from .forms import CustomUserCreationFrom

# Create your views here.


class HomePageView(generic.TemplateView):
    template_name = "home.html"


class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationFrom
    success_url = reverse_lazy("login")
    template_name = "signup.html"

