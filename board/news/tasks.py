# from celery import shared_task
# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
#
# from news.models import Post, Category
# from datetime import datetime
# from django.core.mail import EmailMultiAlternatives
# from board import settings
#
# from django.template.loader import render_to_string
#
#
#
#
# @shared_task
# def every_week_job():
#     today = datetime.datetime.now()
#     last_week = today - datetime.timedelta(days=7)
#     posts = Post.objects.filter(dateCreation__gte=last_week)
#     categories = set(posts.values_list('postCategory__name', flat=True))
#     subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribe__email'))
#
#     html_content = render_to_string(
#         'daily_posts.html',
#         {
#             'link': settings.SITE_URL,
#             'posts': posts
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject='Статьи за неделю',
#         body='',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=subscribers,
#
#     )
#
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()
#
# @shared_task
# def send_notifications(preview, pk, title, subscribe):
#     html_content = render_to_string(
#         'post_created_email.html',
#         {
#             'text': preview,
#             'link': f'{settings.SITE_URL}/news/{pk}'
#         }
#     )
#     msg = EmailMultiAlternatives(
#         subject=title,
#         body='',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=subscribe,
#
#     )
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()
#
#
# @receiver(m2m_changed, sender=Post)
# def notify_about_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.postCategory.all()
#         subscribe_email = []
#
#         for cat in categories:
#             subscribers = cat.subscribe.all()
#             subscribe_email += [s.email for s in subscribers]
#
#         send_notifications(instance.preview(), instance.pk, instance.title, subscribe_email)