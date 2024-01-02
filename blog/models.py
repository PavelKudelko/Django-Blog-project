from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey("article", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} on '{self.article}'"


class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.TextField(max_length=50, default="anonym")
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='blog_post')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:article-detail", kwargs={"pk": self.pk})
