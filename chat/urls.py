from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  # Index page URL
    path("login/", views.login_view, name="login"),  # We'll define this view next
    # dm endpoint with the username as a parameter
    path("dm/", views.dm, name="dm"),
]
