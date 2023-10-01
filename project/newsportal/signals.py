from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import News, Subscriber, Category
from newsportal.tasks import new_post



@receiver(post_save, sender=News)
def news_created(sender,instance, created, **kwargs):
    if created:
        new_post.delay(instance.id, instance.name, instance.text)

































