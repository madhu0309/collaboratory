from django.contrib import admin
from django.urls import path, include
from collab_app import views
from users.views import HomePageView
from django.conf.urls import url

app_name = "collab_app"

# Class Based Views
urlpatterns = [
    # path("", views.QuestionListView.as_view(), name="question-list"),
    url(r"^collab/$", views.question_list_view, name="question-list"),
    # path("", views.question_list_view, name="question-list"),
    path(
        "detail/<int:question_id>/", views.question_detail_view, name="question-detail"
    ),
    # path(
    #     "detail/<slug:slug>/",
    #     views.QuestionDetailView.as_view(),
    #     name="question-detail",
    # ),
    path("questionform/", views.QuestionCreate.as_view(), name="add-question"),
    path(
        "<slug:slug>/edit", views.QuestionUpdateView.as_view(), name="question-update"
    ),
    path(
        "<slug:slug>/delete", views.QuestionDeleteView.as_view(), name="question-delete"
    ),
    path("comment/", views.add_comment_view, name="add-comment"),
    path("env/", views.get_env, name="env"),
]

# Function_Based_Views
# urlpatterns = [
#     path("", views.question_list_view, name="question-list"),
# ]
