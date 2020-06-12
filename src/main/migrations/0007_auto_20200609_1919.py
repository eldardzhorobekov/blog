# Generated by Django 3.0.7 on 2020-06-09 19:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_post_read_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='read_by',
        ),
        migrations.AddField(
            model_name='post',
            name='read_by',
            field=models.ManyToManyField(blank=True, null=True, related_name='read_by', to=settings.AUTH_USER_MODEL),
        ),
    ]