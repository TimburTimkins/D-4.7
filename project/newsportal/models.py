from django.db import models
from django.urls import reverse


class News(models.Model):

    News = 'News'
    Article = 'Article'
    CATEGORY_CHICES = (
        (News, 'News'),
        (Article, 'Article')
    )

    name = models.CharField(
        max_length=50,
        unique=True,
    )
    category = models.CharField(max_length=7, choices=CATEGORY_CHICES, default=News)
    text = models.TextField()
    date_on = models.DateField(auto_now_add = True)

    def __str__(self):
        return f'{self.name.title()}: {self.text} {self.date_on}'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

