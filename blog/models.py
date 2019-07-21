from django.db import models
from django.utils import timezone


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Tag(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Post(models.Model):
    # tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    # comment = models.ForeignKey(Comment, on_delete=models.CASCADE, default=0)
    title = models.CharField(max_length=200)
    text = models.TextField()
    photo = models.ImageField(upload_to='photo', blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
