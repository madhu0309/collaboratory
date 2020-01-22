from django.contrib import admin
from django.urls import path, include
from collab_app import views

app_name = 'collab_app'

urlpatterns = [
    path('',views.QuestionListView.as_view(), name = 'question-list'),
    #path('detail/<int:pk>/',views.QuestionDetailView.as_view(), name = 'question-detail'),
    path('detail/<int:question_id>/',views.question_detail_view,name='question-detail'),
    #path('answerform/<int:question_id>/', views.add_answers, name = 'add-answer'),
    path('questionform/', views.add_question, name = 'add-question'),
    path('register/', views.register, name = 'register'),
    path('logout/', views.logout_request, name='logout'),
    path("login/", views.login_request, name="login"),
    path("env/", views.get_env, name="env"),
]
