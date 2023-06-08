from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Response

#когда только появилось
@receiver(pre_save, sender=Response)
def my_handler(sender, instance, created, **kwargs):
    mail = instance.article.author.email
    send_mail(
        'Subject here',
        'Here is the message.',
        ' host@mail.ru ',
        [mail],
        fail_silently=False,
    )

#когда отклик приняли
@receiver(pre_save, sender=Response)
def my_handler(sender, instance, created, **kwargs):
    if instance.status is True:
        mail = instance.resp_author.email
        send_mail(
            'Subject here',
            'Here is the message.',
            ' host@mail.ru ',
            [mail],
            fail_silently=False,
        )