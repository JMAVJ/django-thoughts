from django.urls import path
from . import views


urlpatterns = [
    path('', views.auth),
    path('/register', views.register),
    path('/logout', views.end_session),
    path('/update-password', views.update_password),
]
