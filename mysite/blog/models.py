from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    likes = models.IntegerField(default=0)  # Track the number of likes
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)  # Track users who liked the post

    def __str__(self):
        return self.title
