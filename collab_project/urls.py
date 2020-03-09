"""collab_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import HomePageView
from django.conf import settings

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    # User management
    # path("accounts/", include("django.contrib.auth.urls")),
    # Local apps
    path("accounts/", include("allauth.urls")),
    path("", include("users.urls")),
    path("collab/", include("collab_app.urls"),),  # , "collab_app")),
    path("formset/", include("formset_app.urls"),),
    path("snippets/", include("snippets.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
