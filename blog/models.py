from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, AbstractUser
from ckeditor.fields import RichTextField
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return str(self.user)


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


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
    content = RichTextField(blank=True, null=True)
    # content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    snippet = models.CharField(max_length=200, blank=True, null=True)
    categories = models.ManyToManyField("Category", related_name="posts")
    likes = models.ManyToManyField(User, related_name='blog_post')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:article-detail", kwargs={"pk": self.pk})

