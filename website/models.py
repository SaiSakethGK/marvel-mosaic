from django.db import models
from django.contrib.auth.models import User


class FavoriteCharacter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    character_id = models.IntegerField()

    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    character_id = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)