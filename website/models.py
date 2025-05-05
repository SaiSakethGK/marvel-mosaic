from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribe_news = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class FavoriteCharacter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    character_id = models.IntegerField()
    rank = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'character_id')

    
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
