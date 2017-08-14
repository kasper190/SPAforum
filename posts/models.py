from django.conf import settings
from django.db import models
from forum.models import Thread


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    publish = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ['publish']

    def __str__(self):
        return str(self.id)


class Note(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notes')
    note = models.TextField()
    publish = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ['publish']

    def __str__(self):
        return str(self.id)