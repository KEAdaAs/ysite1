from django.contrib.auth.models import User
from django.db import models


class Poem (models.Model):
    ended = models.BooleanField(default=False)
    name = models.CharField(max_length=30)


class abzats(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE)


class Otziv(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE)
    text = models.TextField()