from django.conf import settings
from django.db.models.signals import post_save, pre_save, m2m_changed, pre_delete, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Response


def send_response(resp_text, resp_post):
    html_content = render_to_string(
        'created_response.html',
        {
           'text': resp_text,
           # 'author': resp_author,
           'post': resp_post.title,
           'link': f'{settings.SITE_URL}/board/{resp_post.pk}'
        }
    )
    # resp_email = resp_author.email
    msg = EmailMultiAlternatives(
        subject = resp_post.title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[resp_post.author.email]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(post_save, sender=Response)
def create_response(instance, created, **kwargs):
    if created:
        # print('Нью коммент')
        send_response(instance.resp_text, instance.resp_post)


def send_positive_response(resp_text, resp_post, resp_author):
    html_content = render_to_string(
        'positive_response.html',
        {
           'text': resp_text,
           # 'author': resp_author,
           'post': resp_post.title,
           'link': f'{settings.SITE_URL}/board/{resp_post.pk}'
        }
    )
    # resp_email = resp_author.email
    msg = EmailMultiAlternatives(
        subject = resp_post.title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[resp_author.email]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(post_save, sender=Response)
def positive_response(instance, created, **kwargs):
    if instance.status == True:
        # print('Нью коммент')
        send_positive_response(instance.resp_text, instance.resp_post, instance.resp_author)
    else:
        pass
