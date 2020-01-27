from django.contrib import admin
from django.urls import path, include
from collab_app import views
from users.views import HomePageView

app_name = "collab_app"

urlpatterns = [
    path("", views.QuestionListView.as_view(), name="question-list"),
    path(
        "detail/<slug:slug>/",
        views.QuestionDetailView.as_view(),
        name="question-detail",
    ),
    # path(
    #     "detail/<int:question_id>/", views.question_detail_view, name="question-detail"
    # ),
    # path('answerform/<int:question_id>/', views.add_answers, name = 'add-answer'),
    # path("questionform/", views.add_question, name="add-question"),
    path("questionform/", views.QuestionCreate.as_view(), name="add-question"),
    path(
        "<slug:slug>/edit", views.QuestionUpdateView.as_view(), name="question-update"
    ),
    path(
        "<slug:slug>/delete", views.QuestionUpdateView.as_view(), name="question-delete"
    ),
    path("ajax_calls/search/", views.autocompleteModel),
    # # path('register/', views.register, name = 'register'),
    # # path('logout/', views.logout_request, name='logout'),
    # # path("login/", views.login_request, name="login"),
    # path("env/", views.get_env, name="env"),
]
