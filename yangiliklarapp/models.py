from django.db import models
from django.utils import timezone
from rest_framework.authtoken.admin import User


class Category(models.Model):
    name = models.CharField(max_length=150)
    objects = models.Manager()

    def __str__(self):
        return self.name


class NewsModel(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField(null=True)
    image = models.ImageField(null=True, blank=True, upload_to='images')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)
    publish_time = models.DateTimeField(default=timezone.now())
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        ordering = ["-publish_time"]

    def __str__(self):
        return self.title
