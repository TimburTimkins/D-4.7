from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class News(models.Model):

    NEWS = 'NEW'
    ARTICLES = 'ARTICLE'
    TYPES = (
        (NEWS, ('NEW')),
        (ARTICLES, ('ARTICLE'))
    )

    name = models.CharField(
        max_length=50,
        unique=True,
    )
    type = models.CharField(max_length=8, choices=TYPES, default=ARTICLES, unique=False)
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    date_on = models.DateField(auto_now_add = True)

    def __str__(self):
        return f'{self.name.title()}: {self.text} {self.date_on}'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


class Category(models.Model):
    name = models.CharField(max_length=100, unique=False)

    def __str__(self):
        return self.name.title()


class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )

