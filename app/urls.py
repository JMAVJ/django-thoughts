from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('thoughts', views.thoughts),
    path('new-thought', views.add_thought),
    path('thoughts/<int:id>', views.thought),
    path('like-post', views.like_post),
    path('unlike-post', views.unlike_post),
    path('delete-thought', views.delete_thought),
]
