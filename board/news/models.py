# import Article
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128, unique=True)
    text = models.TextField()
    upload = models.FileField(upload_to='uploads/')
    # art = Post.objects.first()
    # art.upload.url #для отображения картинки в шаблоне

    # def __str__(self):
    #     return f'{self.name.title()}: {self.description[:10]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def preview(self):
        return '{} ... {}'.format(self.text[0:123], )

    def __str__(self):
        return f'{self.title}'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Response(models.Model):
    resp_author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    resp_post = models.ForeignKey(Post, on_delete=models.CASCADE) #связь с статьей
    status = models.BooleanField(default=False) #для статуса заявки

    def __str__(self):
        return f'{self.text}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.resp_post.id)])


