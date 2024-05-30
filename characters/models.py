from django.db import models
from django.conf import settings

# Create your models here.
class Character(models.Model):
    name = models.TextField()
    image = models.URLField()
    genre = models.TextField()
    species = models.TextField()
    status =  models.TextField()


    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    character = models.ForeignKey('characters.Character', related_name='votes', on_delete=models.CASCADE)
    