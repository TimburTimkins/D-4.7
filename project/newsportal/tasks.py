from celery import shared_task
import datetime
from newsportal.signals import *
from newsportal.models import News, Subscriber, Category
from django.core.mail import EmailMultiAlternatives


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