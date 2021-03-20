from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    created_by = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE)
    message = models.TextField(max_length=200)
    liked_by = models.ManyToManyField(User, related_name='liked_posts')
