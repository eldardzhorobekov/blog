from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from main.models import Post
from main.utils import send_mail_async


@receiver(post_save, sender=Post)
def send_mail_when_post_created(sender, instance, created, **kwargs):
    if created:
        subject = 'Новый пост в вашей ленте!'
        link = reverse('post-details', kwargs={'pk': 3})
        html_content = 'Автор <b>%s</b> создал новый пост: ' \
                       '<a href="%s">%s</a>' % (
                            instance.author,
                            link,
                            instance.title)
        recievers = instance.author.subscriptions.values_list(
            'email', flat=True)
        send_mail_async(subject, html_content, recievers)
