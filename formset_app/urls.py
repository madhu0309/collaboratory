from django.urls import path, include
from formset_app import views

app_name = "formset_app"

urlpatterns = [
    # path("", views.index, name="formindex"),
    path("prog/<int:programmer_id>", views.progview, name="prog"),
    # path("example/", views.manage_albums, name="manage"),
    path("create_model/", views.create_book_model_form, name="model"),
    path("create_normal/", views.create_book_normal, name="normal"),
    path(
        "create_with_author/",
        views.create_book_with_authors,
        name="model_with_authors",
    ),
    path("book/<int:book_id>", views.authorinlineview, name="inline"),
]
