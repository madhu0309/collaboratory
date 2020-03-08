from django.contrib import admin
from django.urls import path, include
from collab_app import views
from users.views import HomePageView
from django.conf.urls import url
from rest_framework import routers


app_name = "collab_app"

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)


# Class Based Views
urlpatterns = [
    path("", views.QuestionListView.as_view(), name="question-list"),
    # path("search/", views.question_list_view, name="question-search"),
    path(
        "detail/<int:question_id>/", views.question_detail_view, name="question-detail"
    ),
    path(
        "detail/<slug:slug>/",
        views.QuestionDetailView.as_view(),
        name="question-detail",
    ),
    path("questionform/", views.QuestionCreateView.as_view(), name="add-question"),
    path("answerform/<int:pk>/", views.AnswerCreateView.as_view(), name="add-answer"),
    path(
        "commentform/<int:pk>/", views.CommentCreateView.as_view(), name="add-comment",
    ),
    path(
        "<slug:slug>/edit", views.QuestionUpdateView.as_view(), name="question-update"
    ),
    path(
        "<slug:slug>/delete", views.QuestionDeleteView.as_view(), name="question-delete"
    ),
    path("ques-upvote/<int:question_id>/", views.ques_upvote, name="ques-upvote"),
    path("ques-downvote/<int:question_id>/", views.ques_downvote, name="ques-downvote"),
    path("upvote/<int:answer_id>/", views.upvote, name="upvotes"),
    path("downvote/<int:answer_id>/", views.downvote, name="downvotes"),
    path("comment/", views.add_comment_view, name="add-comment"),
    path("hitcount/", include(("hitcount.urls", "hitcount"), namespace="hitcount")),
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

# Function_Based_Views
# urlpatterns = [
#     path("", views.question_list_view, name="question-list"),
# ]
