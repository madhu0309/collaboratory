from django.urls import path
from django.conf.urls import include
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

# urlpatterns = [
#     path("", views.snippet_list),
#     path("<int:pk>/", views.snippet_detail),
#     path("users/", views.UserList.as_view()),
#     path("users/<int:pk>", views.UserDetail.as_view()),
# ]
urlpatterns = format_suffix_patterns(
    [
        path("", views.api_root),
        path("snip/", views.SnippetList.as_view(), name="snippet-list"),
        path("snip/<int:pk>/", views.SnippetDetail.as_view(), name="snippet-detail"),
        path(
            "snip/<int:pk>/highlight/",
            views.SnippetHighlight.as_view(),
            name="snippet-highlight",
        ),
        path("users/", views.UserList.as_view(), name="customuser-list"),
        path("users/<int:pk>/", views.UserDetail.as_view(), name="customuser-detail"),
    ]
)
# urlpatterns += [
#     path("api-auth/", include("rest_framework.urls")),
# ]
