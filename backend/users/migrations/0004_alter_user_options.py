# Generated by Django 4.2.1 on 2023-05-15 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_follow_unique_followed_follower_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('username',), 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
