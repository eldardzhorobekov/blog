from django.core.signals import request_finished
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Post


@receiver(post_save, sender=Post)
def send_mail_when_post_created(sender, instance, created, **kwargs):
    if created:
        subject = 'Новый пост в вашей ленте!'
        message = 'Автор <%s> создал новый пост: %s' % (
            instance.author, instance.title)
        from_email = settings.EMAIL_HOST_USER
        recievers = instance.author.subscriptions.values_list(
            'email', flat=True)
        if recievers.count() > 0:
            send_mail(
                subject, message, from_email, recievers, fail_silently=False
            )


@receiver(request_finished)
def my_callback(sender, **kwargs):
    print('Request finished!')
