from django.urls import path, include
from formset_app import views


urlpatterns = [
    # path("", views.index, name="formindex"),
    path("prog/<int:programmer_id>", views.progview, name="prog"),
    # path("example/", views.manage_albums, name="manage"),
    path("medium/", views.create_book_model_form, name="medium"),
]
