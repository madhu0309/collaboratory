from django.urls import path, include
from formset_app import views


urlpatterns = [
    path("", views.index, name="formindex"),
    path("prog/<int:programmer_id>", views.progview, name="prog"),
]
