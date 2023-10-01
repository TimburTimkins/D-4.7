from celery import shared_task
import datetime
from newsportal.signals import *
from newsportal.models import News, Subscriber, Category
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# @shared_task
# def send_notifications(preciew, pk, title, subsribers):
#

@shared_task
def new_post_notify(instance_id):
    last_week = datetime.datetime.now() - datetime.timedelta(days=7)
    news = News.objects.filter(date_on__gte=last_week)
    categories = set(news.values_list('category', flat=True))
    subscribers = set(Subscriber.objects.filter(category__in=categories))

    for subscriber in subscribers:
        news_subscriber = news.filter(category=subscriber.category)
        text = '\n'.join([f'{n.name} - {n.text}' for n in news_subscriber])

        html_content = (
            f'Название: {News.name}<br>'
            f'Тип: {News.type}<br><br>'

            f'Ссылка на пост</a>'
        )

        msg = EmailMultiAlternatives(
            subject='Посты за неделю',
            body=text,
            to=[subscriber.user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

@shared_task
def new_post(instance, created, text, **kwargs):
    if not created:
        return
    emails = User.objects.filter(
        subscriptions__category=instance.category
    ).values_list('email', flat=True)

    subject = f'Новый пост в категории {instance.category}'
    text_content = (
        f'Название: {instance.name}\n'
        f'Текст: {instance.text}\n\n'
        f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Название: {instance.name}<br>'
        f'Текст: {instance.text}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на пост</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


    # instance = News.objects.get(pk=instance_id)
    # categories = instance.post_category.all()
    # subscribers = []
    #
    # for category in categories:
    #     subscribers += category.subscribers.all()
    #
    # subscribers = list(set(sub.email for sub in subscribers))
    # print(subscribers)
    #
    # for mail in subscribers:
    #     html_content = render_to_string(
    #         'news_edit.html',
    #         {'text': instance.preview, 'link': f' {SITE_URL}/news/{instance_id}'}
    #     )
    #
    #     msg = EmailMultiAlternatives(
    #         subject = instance.name,
    #         body = '',
    #         to = [mail]
    #     )
    #
    #     msg.attach_alternative(html_content, 'text/html')
    #     msg.send()