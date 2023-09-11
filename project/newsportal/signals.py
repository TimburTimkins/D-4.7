from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import News, Subscriber, Category
from newsportal.tasks import new_post_notify



# def news_created(instance, created, **kwargs):
#     if not created:
#         return
#
#     emails = User.objects.filter(
#         subscriptions__category=instance.category
#     ).values_list('email', flat=True)
#
#     subject = f'Новый пост в категории {instance.category}'
#
#     text_content = (
#         f'Название: {instance.name}\n'
#         f'Тип: {instance.type}\n\n'
#         f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
#     )
#     html_content = (
#         f'Название: {instance.name}<br>'
#         f'Тип: {instance.type}<br><br>'
#         f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
#         f'Ссылка на пост</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()

@receiver(post_save, sender=News)
def news_created(sender,instance,  **kwargs):
    if kwargs['action'] == 'news_created':
        category = instance.category.all()
        subscribers: list[str] = []
        for i in category:
            subscribers += i.subscribers.all()
        subscribers = [s.email for s in subscribers]
        print(f'{subscribers = }')

        new_post_notify.delay(instance.preview(), instance.pk, instance.name, subscribers)
































